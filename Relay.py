from queue import Queue
from typing import List, Optional

from Persona import Persona
from Connector import Connector 

# an object that's purpose is to relay output from AI's to the connector and to other AI's 
class Relay:
    def __init__(
            self, 
            connector: Connector, 
            links: List[Persona] = [],
            subscribers: Optional[List[Persona]] = []
        ):
        
        # 1 relay can only have 1 connector
        self._connector = connector

        # can have multiple links (each is two-way comms with a persona)
        self.links = links

        # can have multiple subscribers (each is one way comms with a persona)
        self.subscribers = subscribers

        # temp data storage of a message
        self.message_queue = Queue(-1)

    # Public interfaces
    def submit_prompt(self, prompt):
        responses = []
        for link in self.links:
            responses.append(link.generate_content(prompt))
        response = process_responses(responses)
        return self._transmit(response)
    
    def deposit_message(self, message):
        self.message_queue.put(message)

    def withdraw_message(self):
        self.message_queue.get()

    # transmit the response to the connector, which returns data
    def _transmit(self, response):
        data = self._connector.get_data(response)

        # broadcast will send the response and the data on to other subscribed personas and relays if configured
        # required responses from subscribers to this relay should be returned via the message queue
        self._broadcast(data)

        # return the response and the data to the prompter
        return response, data

    # broadcast the data from the connector to subscribers
    def _broadcast(self, data):
        for subscriber in self.subscribers:
            subscriber.forward(data)


# Place holder for responses processor - just use the first one
def process_responses(responses):
    return responses[0]