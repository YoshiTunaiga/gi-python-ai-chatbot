import openai
from dotenv import load_dotenv
import os


load_dotenv()
client = openai.OpenAI()

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
# Set the message system
PERSONA = "You are a Senior developer with a passion for teaching code and AI who is always eager to help others learn."
MESSAGE_SYSTEM = "A Senior developer with a passion for teaching code and AI."
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]

# Function that moderates user input based on the content
def moderate(user_input):
    response = client.moderations.create(input=user_input)
    return response.results[0].flagged

# Function that generates chat completion
def generate_chat_completion(user_input, messages):
    flagged = moderate(user_input)
    # print(f"Flagged: {flagged}")
    if flagged:
        return ":red[Your comment has been flagged as inappropriate.]"
    completion = client.chat.completions.create(
        model=MODEL_ENGINE,
        messages=messages,
        temperature=1,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return completion.choices[0].message.content
