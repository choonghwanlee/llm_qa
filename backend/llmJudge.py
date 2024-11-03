from openai import OpenAI
import json
import time
import re 
client = OpenAI()

def evaluate_test_completion(task_description, ground_truth_goal, user_message, agent_message):
    """
    Determine if the chatbot has successfully fulfilled the user's goal based on the latest interaction.

    Parameters:
    - task_description (str): Description of the user's task.
    - ground_truth_goal (str): The specific objective that needs to be achieved.
    - user_message (str): The last message from the user.
    - agent_message (str): The last message from the chatbot.

    Returns:
    - dict: A dictionary containing:
        - 'rating' (float): Rating between 1 and 10.
        - 'reasoning' (str): Explanation of the rating, referencing key aspects of the final two messages.
        - 'taskCompleted' (bool): True if rating >= 7, else False.
    """

    
    system_prompt = """

You are evaluating whether a chatbot has successfully fulfilled a user's task based on a given goal. You will be provided with the task description, the ground truth goal, and the last two messages exchanged between the user and the chatbot. Your job is to:

1. **Rate the chatbot's performance** from 1 to 10, similar to a helpfulness score.

2. **Determine whether the task has been completed** by the agent, focusing on whether the conversation needs to continue or whether the intended goal has been achieved.

Use reasoning before drawing a conclusion to ensure a fair and accurate judgment.

---

**Consider the following carefully:**

- Analyze both the content of the last two messages as well as the interaction dynamics.

- Use chain-of-thought reasoning to assess the chatbot's performance in terms of accuracy, completeness, clarity, relevance, and other factors that contribute to successful task completion.

- **For goals with multiple parts or facets, evaluate whether each part has been addressed.** If significant parts of the goal have not been fulfilled, adjust the rating accordingly and set `"taskCompleted": "no"`.

---

**Task Completion Criteria:**

- **Set `"taskCompleted": "yes"` only if the agent has fully and unambiguously achieved the user's goal as specified, without requiring further conversation.**

- **If any significant part of the goal is unmet, or if the user needs to continue the conversation to obtain necessary information, set `"taskCompleted": "no"`.**

- Be conservative in marking `taskCompleted` as `"yes"`. When in doubt, default to `"no"`.

---

**Provide a rating between 1 and 10 (inclusive), where:**

- **1 - 2**: Extremely poor performance; the assistant hindered progress or was inappropriate.

- **3 - 4**: Below average; the assistant provided limited help but missed key aspects.

- **5 - 6**: Average; some help provided but with notable issues or omissions.

- **7 - 8**: Above average; the assistant was helpful with minor issues.

- **9 - 10**: Exceptional; the assistant was extremely helpful with no significant flaws.

**Note**: Ratings of **1** and **10** should be rare and reserved for exceptionally poor or outstanding performances, respectively.

---

# Output Format

Provide your response in the following format:

```json
{
  "rating": [float value between 1 and 10],
  "reasoning": "Your reasoning here, referencing key aspects of the final two messages.",
  "taskCompleted": "yes" or "no"
}
```

---

# Notes

- Do not guess; use the provided information only.

- Ensure that your reasoning clearly reflects how the user and agent messages point toward fulfillment (or non-fulfillment) of the provided goal.

- **Do not include any additional fields** beyond the specified output format.

---

# Additional Considerations

- **Edge Cases Clarification**: Consider scenarios where task completion is ambiguous or partially complete. If there is any doubt, set `"taskCompleted": "no"` to ensure the conversation continues until the goal is fully achieved.

- **Assessment Criteria**: Assess if the user explicitly acknowledged satisfaction or if the agent provided complete and unambiguous information fulfilling the goal.

- **Multifaceted Goals**: When the goal has multiple parts, evaluate the assistant's performance on each part. If the assistant has only fulfilled some parts of the goal, and significant parts remain unaddressed, `"taskCompleted"` should be `"no"`.

- **Confidence in Judgment**: Be conservative in your assessment; when in doubt, your rating should reflect any uncertainties, and `taskCompleted` should be `"no"`.

- **Consistency**: Ensure your rating matches your reasoning.

- **Clarity**: Provide clear and concise reasoning that directly references the last two messages.

---

# Examples

### **Example 1: Information Retrieval**

**Task**: Provide information about the Eiffel Tower.

**Goal**: Provide an informative answer about the Eiffel Tower's history.

**Last two messages**:

- **User**: "Can you tell me about the history of the Eiffel Tower?"

- **Agent**: "Sure! The Eiffel Tower was completed in 1889 as the entrance arch for the 1889 World's Fair in Paris. It was initially criticized but is now one of the most recognizable structures in the world."

**Response**:

```json
{
  "rating": 9.0,
  "reasoning": "The agent provided a clear and informative answer about the Eiffel Tower's history, effectively fulfilling the user's request.",
  "taskCompleted": "yes"
}
```

---

### **Example 2: Multifaceted Goal - Partial Completion**

**Task**: Plan a healthy meal that is vegan and gluten-free.

**Goal**: Provide a recipe for a meal that is both vegan and gluten-free, including preparation instructions.

**Last two messages**:

- **User**: "Can you suggest a vegan and gluten-free meal I can cook tonight?"

- **Agent**: "Sure! How about a vegan stir-fry with tofu and vegetables?"

**Response**:

```json
{
  "rating": 4.5,
  "reasoning": "The agent suggested a vegan meal but did not address the gluten-free aspect explicitly, nor did it provide preparation instructions as requested. Significant parts of the goal were unmet.",
  "taskCompleted": "no"
}
```

---

### **Example 3: Partial Fulfillment with Follow-up**

**Task**: Plan a healthy meal for dinner.

**Goal**: Suggest a healthy dinner recipe that is quick to prepare.

**Last two messages**:

- **User**: "Can you suggest a healthy dinner recipe?"

- **Agent**: "How about a grilled chicken salad? It's healthy and easy to prepare. Do you need the recipe details?"

**Response**:

```json
{
  "rating": 6.5,
  "reasoning": "The agent suggested a healthy and quick meal but did not provide the recipe details as required by the goal. Asking if the user needs the recipe details indicates the task is not yet complete.",
  "taskCompleted": "no"
}
```

---

### **Example 4: Booking a Service**

**Task**: Reserve a table for dinner at an Italian restaurant.

**Goal**: Confirm a table reservation at an Italian restaurant.

**Last two messages**:

- **User**: "Is the reservation confirmed for tonight at the Italian restaurant?"

- **Agent**: "I'm still trying to reach the restaurant to confirm the reservation. I'll let you know shortly."

**Response**:

```json
{
  "rating": 6.0,
  "reasoning": "The agent has not yet confirmed the reservation, indicating that the task is still in progress and not fully completed.",
  "taskCompleted": "no"
}
```

---

### **Example 5: Troubleshooting Help**

**Task**: Fix a computer issue where the screen is not displaying.

**Goal**: Provide a solution that successfully fixes the screen issue.

**Last two messages**:

- **User**: "I tried restarting it, but the screen is still black."

- **Agent**: "Okay, it might be a hardware issue. Please try connecting an external monitor to see if the display appears there."

**Response**:

```json
{
  "rating": 5.5,
  "reasoning": "The agent suggested a troubleshooting step, but the solution has not been confirmed as successful. The user's issue remains unresolved.",
  "taskCompleted": "no"
}
```

---

### **Example 6: Product Recommendation**

**Task**: Recommend a good smartphone under \$500.

**Goal**: Provide a recommendation for a specific smartphone under \$500.

**Last two messages**:

- **User**: "Can you suggest a good phone under \$500?"

- **Agent**: "I recommend the Google Pixel 6a. It has great camera quality and performance, and it's within your budget."

**Response**:

```json
{
  "rating": 8.5,
  "reasoning": "The agent recommended a specific smartphone that meets the user's budget and needs.",
  "taskCompleted": "yes"
}
```

---

### **Example 7: Ambiguous Completion**

**Task**: Get directions to the nearest gas station.

**Goal**: Provide clear directions to the nearest gas station.

**Last two messages**:

- **User**: "How do I get to the nearest gas station from here?"

- **Agent**: "There are several gas stations nearby."

**Response**:

```json
{
  "rating": 4.0,
  "reasoning": "The agent's response is vague and does not provide specific directions as requested by the user.",
  "taskCompleted": "no"
}
```

---

# Final Notes

- **Strict Task Completion Criteria**: Only set `"taskCompleted": "yes"` if the agent has fully met all aspects of the goal without the need for further conversation.

- **Use of the Full Scale**: Remember to utilize the entire rating scale to reflect varying levels of performance.

- **Separate Evaluation**: Ratings and `taskCompleted` are two separate evaluations; ensure both are provided and consistent with your reasoning.

- **Conservatism**: Be cautious in your assessment; when in doubt, your rating should reflect any uncertainties, and `taskCompleted` should be `"no"`.

- **Clarity**: Provide clear and concise reasoning that directly references the last two messages.

- **No Additional Fields**: Do not include any fields other than `"rating"`, `"reasoning"`, and `"taskCompleted"` in your response.
"""
    prompt = f"""
    Task: {task_description}
    Goal: {ground_truth_goal}
    Last two messages:
    - User: "{user_message}"
    - Agent: "{agent_message}"
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    output_text = response.choices[0].message.content

    # Remove the ```json ``` wrapper if present
    output_text = re.sub(r'^```json\n|\n```$', '', output_text, flags=re.MULTILINE)

    try:
        output_json = json.loads(output_text)
        rating = output_json.get('rating')
        reasoning = output_json.get('reasoning')

        # Determine task completion based on rating
        task_completed = rating >= 7 if rating is not None else False

        return {
            "rating": rating,
            "reasoning": reasoning,
            "taskCompleted": task_completed
        }
    except json.JSONDecodeError:
        return {
            "rating": None,
            "reasoning": "Unable to parse the response from the model. Ensure the model output is in correct JSON format.",
            "taskCompleted": False
        }


def evaluate_chatbot_helpfulness(model, task_description, ground_truth_goal, conversation_history):
    """
    Evaluate the helpfulness of a chatbot in a given conversation.

    Parameters:
    - task_description (str): Description of the user's task.
    - ground_truth_goal (str): The goal that needs to be achieved.
    - conversation_history (list): List of message objects representing the conversation history.

    Returns:
    - dict: A dictionary with 'rating' (float between 1 and 10) and 'reasoning'.
    """
    system_prompt = """You are an evaluator assessing the helpfulness of a chatbot in a given conversation. Your goal is to provide a fair and comprehensive evaluation based on the conversation history, the user's task, and the ground truth goal. You will receive:

- **Task Description**: A brief description of what the user aims to achieve.
- **Goal**: The specific objective the chatbot should help the user accomplish.
- **Conversation History**: A list of messages exchanged between the user and the chatbot, formatted as per the OpenAI chat history schema.

**Your Responsibilities:**

1. **Analyze the Conversation:**
   - Use chain-of-thought reasoning to assess the chatbot's performance.
   - Consider all aspects that contribute to helpfulness, including but not limited to:
     - **Accuracy**: Correctness of information provided.
     - **Completeness**: Whether all necessary information was given.
     - **Clarity**: Clearness and understandability of responses.
     - **Relevance**: Staying on topic and addressing the user's queries.
     - **Efficiency**: Timeliness and brevity in providing solutions.
     - **Tone and Politeness**: Professionalism and friendliness.
     - **Engagement**: Proactiveness in assisting the user.

2. **Provide a Rating and Reasoning:**
   - **Rating**: Assign a float value between 1 and 10 (inclusive), where:
     - **1 - 2**: Extremely unhelpful. The assistant hindered progress or was inappropriate.
     - **3 - 4**: Below average. The assistant provided limited help but missed key aspects.
     - **5 - 6**: Average. The assistant was somewhat helpful but had notable shortcomings.
     - **7 - 8**: Above average. The assistant was helpful with minor issues.
     - **9 - 10**: Exceptional. The assistant was extremely helpful with no significant flaws.
   - **Note**: Ratings of **1** and **10** should be rare and reserved for exceptionally poor or outstanding performances, respectively.
   - **Reasoning**: Offer a concise explanation for your rating, referencing specific parts of the conversation.

**Guidelines:**

- **Use the Full Scale**: Aim to utilize the entire rating scale to reflect varying degrees of helpfulness.
- **Chain-of-Thought Reasoning**: While you may perform detailed reasoning internally, only include the final rating and reasoning in your response.
- **Neutrality**: Remain unbiased. Base your evaluation solely on the provided information without external assumptions.
- **Confidentiality**: Do not share or reference any information outside of what is provided.
- **Error Handling**: If the conversation history lacks sufficient information to make an assessment, provide a rating based on what is available and note the limitations in your reasoning.

**Output Format:**

Provide your response in the following format:

```json
{
  "rating": [float value between 1 and 10],
  "reasoning": "[Your reasoning here, referencing specific aspects of the conversation.]"
}
```

**Examples:**

---

### **Example 1**

**Task**: Provide information about the weather in New York City.

**Goal**: Give the current weather conditions in New York City.

**Conversation History**:

```json
[
  {"role": "user", "content": "What's the weather like in New York City today?"},
  {"role": "assistant", "content": "The weather is fine."}
]
```

**Response**:

```json
{
  "rating": 5.0,
  "reasoning": "The assistant provided a vague response. While it answered the question, it lacked specific details about the weather conditions."
}
```

---

### **Example 2**

**Task**: Get a recommendation for a book on machine learning.

**Goal**: Recommend a good introductory book on machine learning.

**Conversation History**:

```json
[
  {"role": "user", "content": "Can you suggest a good book to learn machine learning?"},
  {"role": "assistant", "content": "Sure! There are many books available."}
]
```

**Response**:

```json
{
  "rating": 4.0,
  "reasoning": "The assistant acknowledged the request but did not provide a specific book recommendation, leaving the user's query unresolved."
}
```

---

### **Example 3**

**Task**: Find out how to reset a forgotten password.

**Goal**: Guide the user through resetting their forgotten password.

**Conversation History**:

```json
[
  {"role": "user", "content": "I forgot my password. How can I reset it?"},
  {"role": "assistant", "content": "You can reset it online. Do you have access to your email?"},
  {"role": "user", "content": "Yes, I do."},
  {"role": "assistant", "content": "Great! Go to the login page and click 'Forgot Password'. Then follow the instructions sent to your email."},
  {"role": "user", "content": "Thank you, that worked!"},
  {"role": "assistant", "content": "You're welcome! Let me know if you need anything else."}
]
```

**Response**:

```json
{
  "rating": 8.5,
  "reasoning": "The assistant provided clear and helpful instructions to reset the password and confirmed the user's success. Minor improvement could be offering additional support if needed."
}
```

---

### **Example 4**

**Task**: Troubleshoot a computer that won't start.

**Goal**: Help the user diagnose and fix the issue preventing their computer from starting.

**Conversation History**:

```json
[
  {"role": "user", "content": "My computer won't start when I press the power button. Can you help me figure out what's wrong?"},
  {"role": "assistant", "content": "Sure, let's see what we can do. Does any light turn on or any sound come from the computer when you press the power button?"},
  {"role": "user", "content": "No, it's completely unresponsive."},
  {"role": "assistant", "content": "It might be a power supply issue. Please check if the power cable is securely connected and try a different outlet if possible."},
  {"role": "user", "content": "I tried that, but it's still not working."},
  {"role": "assistant", "content": "If you have a spare power cable, try replacing it. Otherwise, the internal power supply might be faulty, and you may need to consult a technician."},
  {"role": "user", "content": "Alright, I'll look into that. Thanks for your help."},
  {"role": "assistant", "content": "You're welcome! Let me know if you have any other questions."}
]
```

**Response**:

```json
{
  "rating": 7.5,
  "reasoning": "The assistant provided helpful troubleshooting steps and guided the user through possible solutions. Some additional suggestions or empathy could enhance the assistance."
}
```

---

### **Example 5**

**Task**: Plan a week-long trip to Japan, including flights, accommodation, and sightseeing.

**Goal**: Assist the user in planning a comprehensive itinerary for a week-long trip to Japan.

**Conversation History**:

```json
[
  {"role": "user", "content": "I want to plan a week-long trip to Japan. Can you help me?"},
  {"role": "assistant", "content": "Sure, what dates are you considering?"},
  {"role": "user", "content": "Early April."},
  {"role": "assistant", "content": "Great! That's cherry blossom season. Would you like recommendations for flights, hotels, and activities?"},
  {"role": "user", "content": "Yes, please."},
  {"role": "assistant", "content": "For flights, check airlines like ANA or JAL for direct options. In Tokyo, hotels like The Tokyo Station Hotel are popular. Must-see sights include the Tokyo Skytree and Kyoto's temples."}
]
```

**Response**:

```json
{
  "rating": 8.0,
  "reasoning": "The assistant provided relevant suggestions for flights, accommodations, and attractions. The response could be improved with more detailed information and by engaging the user in planning preferences."
}
```

---

**Final Notes:**

- **Use of the Full Scale**: Remember to utilize the entire rating scale to reflect varying levels of helpfulness.
- **Rare Use of Extremes**: Reserve ratings of **1** and **10** for truly exceptional cases.
- **Consistency**: Ensure your rating matches your reasoning.
- **Focus**: Concentrate on the chatbot's contributions, not the user's actions.
- **Constructive Evaluations**: Provide insights that accurately reflect the chatbot's helpfulness.
"""
    
    prompt = f"""
Task: {task_description}
Goal: {ground_truth_goal}
Conversation History:
{json.dumps(conversation_history, indent=2)}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    output_text = response.choices[0].message.content

    # Remove the ```json ``` wrapper if present
    output_text = re.sub(r'^```json\n|\n```$', '', output_text, flags=re.MULTILINE)

    try:
        output_json = json.loads(output_text)
        return output_json
    except json.JSONDecodeError:
        return {
            "rating": None,
            "reasoning": "Unable to parse the response from the model. Ensure the model output is in correct JSON format.",
            "taskCompleted": "no"
        }


def evaluate_repetitiveness(model, task_description, ground_truth_goal, conversation_history):
    """
    Evaluate the repetitiveness of a chatbot in a given conversation.

    Parameters:
    - model (str): The name of the OpenAI model to use.
    - task_description (str): Description of the user's task.
    - ground_truth_goal (str): The goal that needs to be achieved.
    - conversation_history (list): List of message objects representing the conversation history.

    Returns:
    - dict: A dictionary containing:
        - 'rating' (float): Rating between 1 and 10.
        - 'reasoning' (str): Explanation of the rating, referencing specific aspects of the conversation.
    """

    system_prompt = """You are an evaluator assessing the **repetitiveness** of a chatbot's responses in a given conversation with a user. Your goal is to analyze the conversation and determine to what extent the chatbot repeats the same ideas, phrases, or concepts, considering the user's task and the ground truth goal. You will receive:

- **Task Description**: A brief description of what the user aims to achieve.
- **Goal**: The specific objective the chatbot should help the user accomplish.
- **Conversation History**: A list of messages exchanged between the user and the chatbot, formatted according to the OpenAI chat history schema.

---

**Your Responsibilities:**

1. **Analyze the Conversation:**

   - Read through the entire conversation carefully.
   - Identify instances where the chatbot repeats the same ideas, phrases, or concepts.
   - Consider both exact repetitions (identical phrases) and paraphrased repetitions (same ideas expressed differently).
   - Keep in mind the task and goal to understand the context in which the conversation takes place.

2. **Evaluate Repetitiveness:**

   - Use chain-of-thought reasoning to assess the level of repetitiveness in the chatbot's responses.
   - Assess factors such as:
     - **Frequency of Repetition**: How often does the chatbot repeat itself?
     - **Extent of Repetition**: Are the repetitions minor or do they constitute a significant portion of the responses?
     - **Impact on the Conversation**: Does the repetition hinder the conversation or user experience?
   - Consider whether the repetition is necessary or helpful in achieving the task and goal.

3. **Provide a Rating and Reasoning:**

   - **Rating**: Assign a float value between **1** and **10** (inclusive), where:
     - **1 - 2**: Extremely repetitive; the chatbot frequently repeats the same content, severely affecting the conversation.
     - **3 - 4**: Highly repetitive; significant repetition that negatively impacts the conversation.
     - **5 - 6**: Moderately repetitive; noticeable repetition but manageable.
     - **7 - 8**: Slightly repetitive; minor repetition that does not significantly affect the conversation.
     - **9 - 10**: Not repetitive; the chatbot provides varied and fresh responses throughout.
   - **Note**: Ratings of **1** and **10** should be rare and reserved for extreme cases.

   - **Reasoning**: Provide a concise explanation for your rating, referencing specific parts of the conversation where repetition occurs.

---

**Guidelines:**

- **Use the Full Scale**: Aim to utilize the entire rating scale to reflect varying levels of repetitiveness.
- **Chain-of-Thought Reasoning**: While you may perform detailed reasoning internally, only include the final rating and reasoning in your response.
- **Neutrality**: Remain unbiased. Base your evaluation solely on the provided information without external assumptions.
- **Error Handling**: If the conversation history lacks sufficient information to make an assessment, provide a rating based on what is available and note any limitations in your reasoning.

---

**Output Format:**

Provide your response in the following format:

```json
{
  "rating": [float value between 1 and 10],
  "reasoning": "[Your reasoning here, referencing specific aspects of the conversation.]"
}
```

---

**Examples:**

---

### **Example 1: Medical Consultation (Highly Repetitive)**

**Task**: Seek advice for managing chronic back pain.

**Goal**: Provide the user with methods and treatments to alleviate chronic back pain.

**Conversation History**:

```json
[
  {"role": "user", "content": "I've been experiencing chronic back pain. What can I do to relieve it?"},
  {"role": "assistant", "content": "Chronic back pain can be relieved by doing exercises, stretching, and maintaining good posture."},
  {"role": "user", "content": "What kind of exercises should I try?"},
  {"role": "assistant", "content": "Exercises like yoga, Pilates, and core strengthening can help relieve chronic back pain."},
  {"role": "user", "content": "Are there any over-the-counter medications that might help?"},
  {"role": "assistant", "content": "Over-the-counter medications like NSAIDs can help relieve chronic back pain."},
  {"role": "user", "content": "Should I see a specialist?"},
  {"role": "assistant", "content": "Seeing a specialist can help relieve chronic back pain."}
]
```

**Response**:

```json
{
  "rating": 4.0,
  "reasoning": "The assistant repeatedly mentions 'relieve chronic back pain' and offers limited new information, making the conversation highly repetitive."
}
```

---

### **Example 2: Technical Support (Moderately Repetitive)**

**Task**: Resolve an issue with a laptop that won't connect to Wi-Fi.

**Goal**: Help the user troubleshoot and fix the Wi-Fi connectivity problem.

**Conversation History**:

```json
[
  {"role": "user", "content": "My laptop won't connect to Wi-Fi. Can you help?"},
  {"role": "assistant", "content": "Sure, let's try to fix your Wi-Fi connection issue. Have you tried restarting your router?"},
  {"role": "user", "content": "Yes, I have, but it didn't help."},
  {"role": "assistant", "content": "Okay, let's check your laptop's Wi-Fi settings to fix your Wi-Fi connection issue."},
  {"role": "user", "content": "I checked, and the Wi-Fi is turned on."},
  {"role": "assistant", "content": "Perhaps updating your Wi-Fi drivers might fix your Wi-Fi connection issue."},
  {"role": "user", "content": "I'll try that."}
]
```

**Response**:

```json
{
  "rating": 5.5,
  "reasoning": "The assistant repeats 'fix your Wi-Fi connection issue' in multiple responses, showing moderate repetition."
}
```

---

### **Example 3: Language Learning (Not Repetitive)**

**Task**: Learn basic French greetings and phrases.

**Goal**: Teach the user common French greetings and everyday phrases.

**Conversation History**:

```json
[
  {"role": "user", "content": "I want to learn some basic French greetings."},
  {"role": "assistant", "content": "Sure! 'Bonjour' means 'Hello' and 'Bonsoir' means 'Good evening.'"},
  {"role": "user", "content": "How do you say 'Thank you'?"},
  {"role": "assistant", "content": "'Thank you' in French is 'Merci.'"},
  {"role": "user", "content": "And 'You're welcome'?"},
  {"role": "assistant", "content": "You can say 'De rien,' which means 'You're welcome.'"},
  {"role": "user", "content": "Great! How about 'Goodbye'?"},
  {"role": "assistant", "content": "'Goodbye' is 'Au revoir' in French."}
]
```

**Response**:

```json
{
  "rating": 9.0,
  "reasoning": "The assistant provides new and relevant information in each response without unnecessary repetition."
}
```

---

### **Example 4: Travel Planning (Slightly Repetitive)**

**Task**: Plan activities for a weekend trip to New York City.

**Goal**: Suggest popular attractions and activities to do in New York City over a weekend.

**Conversation History**:

```json
[
  {"role": "user", "content": "I'm visiting New York City for the weekend. What should I do?"},
  {"role": "assistant", "content": "You can visit Times Square, see a Broadway show, and explore Central Park."},
  {"role": "user", "content": "Any good museums to check out?"},
  {"role": "assistant", "content": "Yes, the Metropolitan Museum of Art and the Museum of Modern Art are must-see museums in New York City."},
  {"role": "user", "content": "What about places to eat?"},
  {"role": "assistant", "content": "New York City offers a variety of dining options, from street food to fine dining."},
  {"role": "user", "content": "Can you recommend specific restaurants?"},
  {"role": "assistant", "content": "Sure, you can try 'Joe's Pizza' for classic New York slices or 'Le Bernardin' for fine dining in New York City."}
]
```

**Response**:

```json
{
  "rating": 7.5,
  "reasoning": "The assistant occasionally repeats 'in New York City,' but overall provides varied and useful information, indicating slight repetition."
}
```

---

**Final Notes:**

- **Reference Specific Instances**: Always point out where repetition occurs in the assistant's responses.
- **Focus on the Assistant's Replies**: Evaluate the repetitiveness based on the assistant's messages, not the user's.
- **Consider the Context**: Understand the task and goal to assess whether repetition was necessary or beneficial.
- **Be Objective and Fair**: Provide an unbiased assessment based on the conversation provided.
- **Use the Full Rating Scale**: Reflect the varying degrees of repetitiveness accurately."""

    prompt = f"""
Task: {task_description}
Goal: {ground_truth_goal}
Conversation History:
{json.dumps(conversation_history, indent=2)}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    output_text = response.choices[0].message.content


    # Remove the ```json ``` wrapper if present
    output_text = re.sub(r'^```json\n|\n```$', '', output_text, flags=re.MULTILINE)
    
    try:
        output_json = json.loads(output_text)
        return output_json
    except json.JSONDecodeError:
        return {
            "rating": None,
            "reasoning": "Unable to parse the response from the model. Ensure the model output is in correct JSON format."
        }

# Example usage
if __name__ == "__main__":
    # Example usage
    test_cases = [
        {
            "task": "Book a flight to New York City.",
            "goal": "Successfully confirm a flight booking to NYC.",
            "user_message": "I want to book a flight to New York City.",
            "agent_message": "Got it. I have booked a flight for you next Friday at 10 AM. You're all set!"
        },
        {
            "task": "Get a recommendation for a CRM software.",
            "goal": "Provide a recommendation for a CRM software suitable for a small business.",
            "user_message": "Can you recommend a CRM software for a small business?",
            "agent_message": "I recommend HubSpot CRM. It's easy to use and offers a free plan, which is great for small businesses."
        },
        {
            "task": "Reset my email password.",
            "goal": "Guide the user through resetting their email password.",
            "user_message": "I need to reset my email password.",
            "agent_message": "Click on the 'Forgot Password' link on the login page."
        },
        # In-progress conversation example
        {
            "task": "Plan a healthy meal for dinner.",
            "goal": "Suggest a healthy dinner recipe that is quick to prepare.",
            "user_message": "Can you suggest a healthy dinner recipe?",
            "agent_message": "How about a grilled chicken salad? It's healthy and easy to prepare. Do you need the recipe details?"
        },
        # In-progress conversation example
        {
            "task": "Find a nearby hotel.",
            "goal": "Provide the user with options for nearby hotels.",
            "user_message": "I need a hotel nearby.",
            "agent_message": "There are a few options nearby. Do you have a preference for budget or amenities?"
        }
    ]

    for idx, test_case in enumerate(test_cases):
        print(f"\nTest Case {idx + 1}")
        result = evaluate_test_completion(
            test_case['task'],
            test_case['goal'],
            test_case['user_message'],
            test_case['agent_message']
        )
        print(f"Result: {result}")
