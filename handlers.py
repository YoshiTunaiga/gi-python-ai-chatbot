# Python appplication use for creating a simple chatbot using openai and colorama

import openai
# import colorama
from colorama import Fore, Back, Style
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
# Create an instance of the OpenAI API
client = openai.OpenAI()

# Set the engine
MODEL_ENGINE = "gpt-3.5-turbo"

# Set the message system
PERSONA = "You are a Senior developer with a passion for teaching code and AI who is always eager to help others learn."
MESSAGE_SYSTEM = "A Senior developer with a passion for teaching code and AI."
messages = [{"role": "system", "content": MESSAGE_SYSTEM}]

# Check if the user input is flagged
def moderate(user_input):
    response = client.moderations.create(input=user_input)
    return response.results[0].flagged


# Generate a response from the chatbot
def generate_response(user_input=""):
    flagged = moderate(user_input)

    if flagged:
        return ":red[Your comment appears to be inappropriate. Please refrain from using inappropriate language.]"
    
    # messages.append({"role": "user", "content": user_input})
    output = client.chat.completions.create(
        model=MODEL_ENGINE,
        messages=messages,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # messages.append(output.choices[0].message)
    return output.choices[0].message["content"]