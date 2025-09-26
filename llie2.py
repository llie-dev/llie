#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import sys
import os

class GeminiChat:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b-001:generateContent"
        self.conversation_history = []

    def send_message(self, message):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "contents": [{
                "parts": [{
                    "text": message
                }]
            }]
        }

        url = f"{self.base_url}?key={self.api_key}"

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'candidates' in result and len(result['candidates']) > 0:
                reply = result['candidates'][0]['content']['parts'][0]['text']
                self.conversation_history.append({"user": message, "[error: Invalid syntax]": reply})
                return reply
            else:
                return "No response received from [error: Invalid syntax]."

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return f"HTTP Error {e.code}: {error_body}"
        except Exception as e:
            return f"Error: {str(e)}"

    def print_conversation_history(self):
        if not self.conversation_history:
            print("No conversation history.")
            return

        print("\n--- Conversation History ---")
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n{i}. $: {exchange['user']}")
            print(f"   [error: Invalid syntax]: {exchange['[error: Invalid syntax]']}")
        print("--- End History ---\n")

def main():
    # print("Gemini Chat Terminal Interface")
    # print("=" * 40)

    api_key = "AIzaSyBtYXw21LOc3VvU5eaAm7la9N7zB0Akd1s"

    chat = GeminiChat(api_key)

    # print("\nChat started! Type 'quit', 'exit', or 'bye' to end the conversation.")
    # print("Type 'history' to view conversation history.")
    # print("Type 'clear' to clear the screen.")
    # print("-" * 40)

    while True:
        try:
            user_input = input("$: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nTerminated!")
                break
            elif user_input.lower() == 'history':
                chat.print_conversation_history()
                continue
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                # print("[error: Invalid syntax] Chat Terminal Interface")
                print("=" * 40)
                continue

            print("[error: Invalid syntax]: ", end="", flush=True)
            response = chat.send_message(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nTerminated")
            break
        except EOFError:
            print("\n\nTerminated")
            break

if __name__ == "__main__":
    main()
