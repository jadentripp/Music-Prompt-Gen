import os
import anthropic
from termcolor import colored

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class PromptComposer:
    def __init__(self):
        self.model = 'claude-3-opus-20240229'
        self.prompt_file = './prompts/prompt1.txt'

    def load_prompt(self):
        with open(self.prompt_file, 'r') as file:
            return file.read()

    def generate_completion(self, user_input, model_prompt):
        message = anthropic_client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=model_prompt,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return message.content

    def save_output(self, user_input, output):
        path = f"outputs/{self.model}"
        os.makedirs(path, exist_ok=True)
        output_text = ', '.join(block.text for block in output)
        with open(f"{path}/{user_input[:50]}.txt", "w") as file:
            file.write(output_text)

    def run(self):
        model_prompt = self.load_prompt()

        while True:
            user_input = input("\nPlease enter your prompt or 'exit' to quit: ")

            if user_input.lower().strip() == "exit":
                print('Exiting... Goodbye!')
                break

            output = self.generate_completion(user_input, model_prompt)
            print(output)
            self.save_output(user_input, output)

if __name__ == "__main__":
    PromptComposer().run()
