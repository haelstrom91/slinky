import openai
import yaml
from typing import List, Optional

# from Relay import Relay

# a class to capture the idea of an AI adopting a persona
class Persona:
    def __init__(
            self, 
            name: str, 
            model: str, 
            key: str, 
            knowledge: str, 
            # collaborators:List = [], 
            # relays: Optional[List[Relay]] = []
        ):

        # A designation for the Persona
        self.name = name

        # A model for the Persona to use 
        self.model = model

        # An API key for the Persona to use 
        self.key = key

        # A base set of prompts that define the Persona
        self.messages = [
            {
                "role": "system", 
                "content": get_persona_prompt(name)
            },
            {
                "role": "user", 
                "content": knowledge
            },
        ]

        # list of other personas to send output to
        self.collaborators = []

        # list of relays to send output to
        self.relays = relays

    # add a test here for message validity
    def _add_message(self, message):
        self.messages.append(message)

    # main action of an LLM - predict the most likely next message in a conversation
    # openai method only at this stage 
    def generate_content(self, prompt):
        openai.api_key = self.key
        # add the prompt as a message by the user role
        self._add_message(
            {
                "role": "user",
                 "content": prompt
            }
        )
        # send the request to the API
        response = openai.ChatCompletion.create(
            model = self.model,
            # self.temperature=0.6,
            messages = self.messages
        )
        # Add the response content as a message by the assistant 
        response_content = response.choices[0].message.content
        self._add_message(
            {
                "role": "assistant",
                "content": response_content
            }
        )
        return response_content

    def reply(self, prompt):
        response_content = self.generate(prompt)
        return response_content

    # openai specific method currently
    def forward(self, prompt):
        response_content = self.generate(prompt)
        for collaborator in self.collaborators:
            collaborator.prompt(response_content)


# Pre-condition: file named '{name}.txt' added to the prompts folder containing the system prompt to create the persona
def get_persona_prompt(name):
    with open(f'prompts/{name}.txt', 'r') as file:
        prompt = file.read()
    return prompt