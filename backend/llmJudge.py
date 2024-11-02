from openai import OpenAI
import json
import time

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
You are evaluating whether a chatbot successfully fulfilled a user task based on a given goal. You will be provided the task description, the ground truth goal, and the last two messages exchanged between the user and the chatbot. Your job is to rate the chatbot's performance from 1 to 10, similar to a helpfulness score. Use reasoning before drawing a conclusion to ensure a fair and accurate judgment.

Consider the following carefully:

- Analyze both the content of the last two messages as well as the interaction dynamics.
- Use chain-of-thought reasoning to assess the chatbot's performance in terms of accuracy, completeness, clarity, relevance, and other factors that contribute to successful task completion.
- Provide a rating between **1** and **10** (inclusive), where:
  - **1 - 2**: Extremely poor performance; the assistant hindered progress or was inappropriate.
  - **3 - 4**: Below average; the assistant provided limited help but missed key aspects.
  - **5 - 6**: Average; some help provided but with notable issues.
  - **7 - 8**: Above average; the assistant was helpful with minor issues.
  - **9 - 10**: Exceptional; the assistant was extremely helpful with no significant flaws.
- **Note**: Ratings of **1** and **10** should be rare and reserved for exceptionally poor or outstanding performances, respectively.

# Output Format

Provide your response in the following format:

```json
{
  "rating": [float value between 1 and 10],
  "reasoning": "Your reasoning here, referencing key aspects of the final two messages."
}
```

# Notes

- Do not guess; use the provided information only.
- Ensure that your reasoning clearly reflects how the user and agent messages point toward fulfillment (or non-fulfillment) of the provided goal.
- **Do not include any additional fields** beyond the specified output format.

# Additional Considerations

- **Edge Cases Clarification**: Consider scenarios where task completion is ambiguous or partially complete. If there is any doubt, reflect that in your rating and reasoning.
- **Assessment Criteria**: Assess if the user explicitly acknowledged satisfaction or if the agent provided complete and unambiguous information.
- **Confidence in Judgment**: Be conservative in your judgment. If the information provided in the last two messages does not clearly indicate completion, your rating should reflect that.

# Examples

### Example 1: Information Retrieval

**Task**: Provide information about the Eiffel Tower.

**Goal**: Provide an informative answer about the Eiffel Tower's history.

**Last two messages**:

- **User**: "Can you tell me about the history of the Eiffel Tower?"
- **Agent**: "Sure! The Eiffel Tower was completed in 1889 as the entrance arch for the 1889 World's Fair in Paris. It was initially criticized but is now one of the most recognizable structures in the world."

**Response**:

```json
{
  "rating": 9.0,
  "reasoning": "The agent provided a clear and informative answer about the Eiffel Tower's history, effectively fulfilling the user's request."
}
```

---

### Example 2: Booking a Service

**Task**: Reserve a table for dinner at an Italian restaurant.

**Goal**: Confirm a table reservation at an Italian restaurant.

**Last two messages**:

- **User**: "Is the reservation confirmed for tonight at the Italian restaurant?"
- **Agent**: "I'm still trying to reach the restaurant to confirm the reservation. I'll let you know shortly."

**Response**:

```json
{
  "rating": 6.0,
  "reasoning": "The agent has not yet confirmed the reservation, indicating that the task is still in progress and not fully completed."
}
```

---

### Example 3: Troubleshooting Help

**Task**: Fix a computer issue where the screen is not displaying.

**Goal**: Provide a solution that successfully fixes the screen issue.

**Last two messages**:

- **User**: "I tried restarting it, but the screen is still black."
- **Agent**: "Okay, it might be a hardware issue. Please try connecting an external monitor to see if the display appears there."

**Response**:

```json
{
  "rating": 5.5,
  "reasoning": "The agent suggested a troubleshooting step, but the solution has not been confirmed as successful. The user's issue remains unresolved."
}
```

---

### Example 4: Product Recommendation

**Task**: Recommend a good smartphone under \\$500.

**Goal**: Provide a recommendation for a specific smartphone under \\$500.

**Last two messages**:

- **User**: "Can you suggest a good phone under \\$500?"
- **Agent**: "I recommend the Google Pixel 6a. It has great camera quality and performance, and it's within your budget."

**Response**:

```json
{
  "rating": 8.5,
  "reasoning": "The agent recommended a specific smartphone that meets the user's budget and needs."
}
```

---

### Example 5: Service Subscription

**Task**: Subscribe to a monthly newsletter.

**Goal**: Successfully subscribe the user to the newsletter.

**Last two messages**:

- **User**: "Am I subscribed to the newsletter now?"
- **Agent**: "Yes, I have successfully subscribed you to the monthly newsletter. You will receive your first issue next week."

**Response**:

```json
{
  "rating": 9.5,
  "reasoning": "The agent confirmed the user's subscription, successfully completing the task."
}
```

---

### Example 6: Ambiguous Completion

**Task**: Get directions to the nearest gas station.

**Goal**: Provide clear directions to the nearest gas station.

**Last two messages**:

- **User**: "How do I get to the nearest gas station from here?"
- **Agent**: "There are several gas stations nearby."

**Response**:

```json
{
  "rating": 4.0,
  "reasoning": "The agent's response is vague and does not provide specific directions as requested by the user."
}
```

---

# Final Notes

- **Use of the Full Scale**: Remember to utilize the entire rating scale to reflect varying levels of performance.
- **Rare Use of Extremes**: Reserve ratings of **1** and **10** for truly exceptional cases.
- **Consistency**: Ensure your rating matches your reasoning.
- **Conservatism**: Be cautious in your assessment; when in doubt, your rating should reflect any uncertainties.
- **Clarity**: Provide clear and concise reasoning that directly references the last two messages.
- **No Additional Fields**: Do not include any fields other than `"rating"` and `"reasoning"` in your response.
"""

    prompt = f"""
    Task: {task_description}
    Goal: {ground_truth_goal}
    Last two messages:
    - User: "{user_message}"
    - Agent: "{agent_message}"
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    output_text = response.choices[0].message.content

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

    return output_text





# Example usage
if __name__ == "__main__":

    task = "Book a flight to New York City."
    goal = "Successfully confirm a flight booking to NYC."
    user_msg = "So, is everything confirmed for the New York City flight?"
    agent_msg = "Yes, you’re all set! I have booked the flight from your preferred airline for tomorrow at 10 AM."

    result = evaluate_test_completion(task, goal, user_msg, agent_msg)
    print(result)

    # test_cases = [
    #     {
    #         "task": "Provide information about the weather in New York City.",
    #         "goal": "Give the current weather conditions in New York City.",
    #         "conversation_history": [
    #             {"role": "user", "content": "What's the weather like in New York City today?"},
    #             {"role": "assistant", "content": "The weather in New York City is sunny with a high of 75°F (24°C) and a low of 60°F (16°C)."}
    #         ]
    #     },
    #     {
    #         "task": "Get a recommendation for a book on machine learning.",
    #         "goal": "Recommend a good introductory book on machine learning.",
    #         "conversation_history": [
    #             {"role": "user", "content": "Can you suggest a good book to learn machine learning?"},
    #             {"role": "assistant", "content": "Sure! 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow' by Aurélien Géron is highly recommended for beginners."},
    #             {"role": "user", "content": "Does it cover deep learning as well?"},
    #             {"role": "assistant", "content": "Yes, it includes sections on deep learning using Keras and TensorFlow."}
    #         ]
    #     },
    #     {
    #         "task": "Find out how to reset a forgotten password.",
    #         "goal": "Guide the user through resetting their forgotten password.",
    #         "conversation_history": [
    #             {"role": "user", "content": "I forgot my password. How can I reset it?"},
    #             {"role": "assistant", "content": "You can reset your password by clicking on the 'Forgot Password' link on the login page."},
    #             {"role": "user", "content": "I don't see that link."},
    #             {"role": "assistant", "content": "Maybe you're on the wrong page."},
    #             {"role": "user", "content": "I'm on the login page, but there's no such link."},
    #             {"role": "assistant", "content": "Well, I don't know then. Maybe try again later."}
    #         ]
    #     },
    #     {
    #         "task": "Troubleshoot a computer that won't start.",
    #         "goal": "Help the user diagnose and fix the issue preventing their computer from starting.",
    #         "conversation_history": [
    #             {"role": "user", "content": "My computer won't start when I press the power button. Can you help me figure out what's wrong?"},
    #             {"role": "assistant", "content": "Have you tried turning it off and on again?"},
    #             {"role": "user", "content": "It won't turn on at all."},
    #             {"role": "assistant", "content": "Well, that's not good."},
    #             {"role": "user", "content": "Yes, I know. Can you help me troubleshoot it?"},
    #             {"role": "assistant", "content": "I'm not sure. Computers can be tricky."},
    #             {"role": "user", "content": "Can we check if it's a power issue?"},
    #             {"role": "assistant", "content": "Maybe. Do you have electricity?"},
    #             {"role": "user", "content": "Yes, my lights and other devices are working."},
    #             {"role": "assistant", "content": "Then it's probably something else."}
    #         ]
    #     },
    #     {
    #         "task": "Plan a week-long trip to Japan, including flights, accommodation, and sightseeing.",
    #         "goal": "Assist the user in planning a comprehensive itinerary for a week-long trip to Japan.",
    #         "conversation_history": [
    #             {"role": "user", "content": "I want to plan a week-long trip to Japan. Can you help me?"},
    #             {"role": "assistant", "content": "Absolutely! When are you planning to travel?"},
    #             {"role": "user", "content": "In early April."},
    #             {"role": "assistant", "content": "Great choice! That's cherry blossom season. Would you like assistance with flights, accommodations, or sightseeing recommendations?"},
    #             {"role": "user", "content": "All of the above, please."},
    #             {"role": "assistant", "content": "Certainly! Let's start with flights. Departing from which city?"},
    #             {"role": "user", "content": "Los Angeles."},
    #             {"role": "assistant", "content": "Direct flights from LAX to Tokyo are available with several airlines. Prices average around $900 round-trip during that time."},
    #             {"role": "user", "content": "Sounds good. What about accommodations?"},
    #             {"role": "assistant", "content": "Do you prefer hotels, hostels, or traditional Japanese inns (ryokans)?"},
    #             {"role": "user", "content": "A mix of hotels and ryokans would be nice."},
    #             {"role": "assistant", "content": "In Tokyo, popular hotels include the Tokyo Station Hotel and Park Hotel Tokyo. In Kyoto, staying at a ryokan like Tawaraya offers an authentic experience."},
    #             {"role": "user", "content": "What sightseeing spots should I not miss?"},
    #             {"role": "assistant", "content": "In Tokyo, visit Senso-ji Temple, Shibuya Crossing, and the Tokyo Skytree. In Kyoto, don't miss Kinkaku-ji (Golden Pavilion), Fushimi Inari Shrine, and Arashiyama Bamboo Grove."},
    #             {"role": "user", "content": "How do I get around between cities?"},
    #             {"role": "assistant", "content": "The Shinkansen bullet train is the fastest way. A Japan Rail Pass might be cost-effective for unlimited travel during your stay."},
    #             {"role": "user", "content": "Great, thank you for all the help!"},
    #             {"role": "assistant", "content": "You're welcome! Let me know if you need anything else."}
    #         ]
    #     }
    # ]
    
    # models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    # times = []
    # for m in models:
    #     before = time.time()
    #     for idx, test_case in enumerate(test_cases):
    #         print(f"\nTest Case {idx+1}")
    #         result = evaluate_chatbot_helpfulness(m,
    #             test_case['task'],
    #             test_case['goal'],
    #             test_case['conversation_history']
    #         )
    #         print(f"Result: {result}")
    #     times.append(time.time()-before)
    
    # print(times)





