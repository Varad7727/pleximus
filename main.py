import os
from dotenv import load_dotenv
from google import genai
from tools import (
    calculator,
    weather,
    text_utility,
    wikipedia_summary,
    currency_converter,
)

# Load environment variables from .env
load_dotenv()

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Enter your Gemini API Key: ").strip()

    client = genai.Client(api_key=api_key)

    # List of callable tools provided to the agent
    tools_list = [
        calculator,
        weather,
        text_utility,
        wikipedia_summary,
        currency_converter,
    ]

    # Create a persistent chat session with tool-calling enabled
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "tools": tools_list,
            "system_instruction": (
                "You are an AI assistant equipped with tools. When a user request "
                "requires a calculation, weather lookup, text operation, Wikipedia summary, "
                "or currency conversion, invoke the corresponding tool."
            ),
        },
    )

    print("==================================================")
    print(" AI Agent Ready! (Type 'exit' or 'quit' to stop)  ")
    print("==================================================")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Exiting agent. Good luck with the submission!")
                break

            response = chat.send_message(user_input)
            print(f"\nAgent: {response.text}")

        except KeyboardInterrupt:
            print("\nExiting agent.")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()