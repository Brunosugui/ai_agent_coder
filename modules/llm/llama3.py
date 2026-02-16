import time
import requests

from modules.llm.base import BaseLLM


class LLama3(BaseLLM):

    url = "http://localhost:11434/api/chat"

    def __init__(self):
        super().__init__("llama3")

    def chat(self, messages):
        payload = {
            "model": self.name,
            "messages": messages,
            "stream": False,
        }

        valid_response = False

        while not valid_response:
            response = requests.post(LLama3.url, json=payload, timeout=120)
            response.raise_for_status()

            content = response.json()["message"]["content"]

            valid_response = len(content.strip()) > 0
            if not valid_response:
                import pdb; pdb.set_trace()
                print("Got empty response, waiting 5s...")
                time.sleep(5)

        return content
