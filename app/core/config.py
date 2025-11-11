import os
import json
from openai import OpenAI
from dotenv import load_dotenv

class Config:

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat_llm_json(self, messages):
        """Chat with llm - json output"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.5,
        )

        return json.loads(response.choices[0].message.content)
    
    def chat_llm(self, messages):
        """chat with llm"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5,
        )

        return response.choices[0].message.content
    
config = Config()