# Python appplication use for creating a simple chatbot using openai and colorama

import openai
import colorama
from colorama import Fore, Back, Style
import os
from dotenv import load_dotenv


load_dotenv()

# Set the API key
# openai.api_key =

# Set the engine
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [{"role": "system", "content": "Hello, I am a chatbot. I am here to help you with your queries."}]

client = openai.OpenAI()

def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=MODEL_ENGINE,
        messages=messages,
    )
    messages.append(response.choices[0].message)
    return response.choices[0].message["content"]

def main():
    colorama.init()
    os.system("cls")
    print(Fore.GREEN + "\n")
    print("----------------------------------------\n")
    print(" *** 🤖 WELCOME TO THE AI-CHATBOT *** ")
    print("\n----------------------------------------")
    print("\n================* MENU *================\n")
    print(Fore.RED + "Type 'exit' to quit the chatbot")

    while True:
        user_input = input(Fore.YELLOW + "You: ")
        if user_input.lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})

         # Step 1: send the conversation and available functions to GPT
        response = generate_response(user_input)
        print(Fore.RED + "Chatbot: " + Fore.WHITE + response.content)
        messages.append({"role": "system", "content": response.content})
    colorama.deinit()

if __name__ == "__main__":
    main()