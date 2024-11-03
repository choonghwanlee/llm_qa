from typing import Union, Optional, List
from models import AITest, Test, RunTest
from prompts import _get_AITest_prompt, _get_persona_prompt
from util import extract_sections
from llmJudge import evaluate_test_completion, evaluate_chatbot_helpfulness, evaluate_repetitiveness
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)


client = OpenAI()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/createManualTest")
def createTest(test: Test):
    '''
    create a new test from user's manual input and add to DB
    '''
    response = (
        supabase.table("LLMQA").insert({'task': test.task, 'goal': test.goal, 'persona': test.persona}).execute()
    )
    return response

@app.post("/createAITest")
async def createAITest(test: AITest):
    new_data = []
    system_prompt = _get_AITest_prompt(test.chatbot_desc)
    completions = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'User Description: {test.user_desc}'}
        ],
        n=test.n_samples, ## default is 4 generations
        max_completion_tokens=256, ## cap tokens generated
    )
    for completion in completions.choices:
        new_data.append(extract_sections(completion.message.content))
    response = (
        supabase.table("LLMQA").insert(new_data).execute()
    )
    return response
    
@app.post("/runTests")
async def runTest(configs: RunTest):
    '''
    main function to run a selected set of tests
    '''
    print('hi')
    seed_prompt = _get_persona_prompt(configs.persona, configs.task)
    user_prompt = _get_persona_prompt(configs.persona, configs.task, generation=True)
    chatbot_system_prompt = f"You are a Zara customer support agent that {configs.chatbot_desc}"
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': seed_prompt},
            {'role': 'user', 'content': 'What is the first thing you will say to the AI agent to start your conversation?'}
        ],
        max_completion_tokens = 128,
    )
    print('seed generated')
    seed_query = completion.choices[0].message.content
    chatbot_messages = [{'role': 'system', 'content': chatbot_system_prompt}, {"role": "user", "content": seed_query}]
    user_messages = [{'role': 'system', 'content': user_prompt}, {"role": "assistant", "content": seed_query}]
    num_sent = 1
    ### while number of turns is less than configs.n_turns
    while num_sent < 10:
        ### get AI response
        ai_response = client.chat.completions.create(
            model = 'gpt-4o-mini',
            messages = chatbot_messages,
            max_completion_tokens = 256,
        )
        print('ai response')
        chatbot_messages.append({'role': 'assistant', 'content': ai_response.choices[0].message.content})
        user_messages.append({'role': 'user', 'content': ai_response.choices[0].message.content})
        num_sent += 1
        ### check if intent is satisfied. break if so
        response = evaluate_test_completion(configs.task, configs.goal, chatbot_messages[-2]['content'], chatbot_messages[-1]['content'])
        print('evals')
        if response['taskCompleted']: break
        ### if not, get human response
        human_response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=user_messages,
            max_completion_tokens = 128,
        )
        print('human response')
        chatbot_messages.append({'role': 'user', 'content': human_response.choices[0].message.content})
        user_messages.append({'role': 'assistant', 'content': human_response.choices[0].message.content})
        num_sent += 1
    ### 
    print('loop exited')
    helpfulness_response = evaluate_chatbot_helpfulness('gpt-4o', configs.task, configs.goal, chatbot_messages[1:])
    repetiveness_response = evaluate_repetitiveness('gpt-4o', configs.task, configs.goal, chatbot_messages[1:])
    print('eval functions')
    print('repetitiveness_metric: ', repetiveness_response['rating'], type(repetiveness_response['rating']))
    print('conversation: ', chatbot_messages)
    print('helpfulness_metric: ', helpfulness_response['rating'], type(helpfulness_response['rating']))
    print('goal_completion_accuracy: ', response['rating'], type(response['rating']))
    print('goal_completion_reasoning: ', response['reasoning'], type(response['reasoning']))
    print('test_id: ', configs.test_id)
    result = (supabase.table("LLMQA").update({'conversation': json.dumps(chatbot_messages[1:]), 'repetitiveness_metric': repetiveness_response['rating'], 
                                     'helpfulness_metric': helpfulness_response['rating'], 'num_exchanges': num_sent, 
                                     'goal_completion_accuracy': response['rating'], 'goal_completion_reasoning': response['reasoning'], 'status': 'Run'}).eq("test_id", configs.test_id).execute()
    )
    return result
