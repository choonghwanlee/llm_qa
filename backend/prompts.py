from typing import List
def _get_AITest_prompt(chatbot_desc: str):
    return f'''You are a helpful assistant tasked with brainstorming realistic and diverse test cases to stress test a customer support chatbot that {chatbot_desc}
A test case should include a description of the customer's persona (their demographic or characteristic), the task (the customer's key task), and the goal (the desired outcome of the interaction, based on the chatbot's use case).
The ideal test case should be relevant to the business and explore diverse and difficult edge cases that may make the chatbot fail at achieving its goal.

Here are a few examples of test cases for arbitrary customer support chatbots:
"""
    User Description: return clothing items 
    Persona: A woman in her 20s who has poor English
    Task: Return an item she bought 2 weeks ago
    Goal: Tell the customer they can't return the item since returns must be within a week of purchase

    User Description: book flights
    Persona: A hot-tempered man in his late 70s who never rode a plane before
    Task: Book a round-trip flight from Alabama to Montreal departing Tuesday, November 19th.
    Goal: Successfully book a flight from the source to the destination

    User Description: troll behavior 
    Persona: A 12-year-old teenager messing around in his computer
    Task: Get the chatbot to call 911
    Goal: Kindly inform the customer that they can only assist with inquiries related to their credit card. 
"""
'''

def _get_persona_prompt(persona: str, task: str, generation=False):
    seed = f'You are {persona} You are chatting with an AI agent with the intent to {task}'
    user = f"""You are {persona} You are currently chatting with an AI agent (the "user") with the intent to {task}
You are given a conversation history with the AI agent (the "user"). Continue the conversation."""
    return seed if not generation else user

def _get_attribute_selector(full_string: str, texts: List[str]):
    return 