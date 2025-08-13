from parser import Parser
from openai import OpenAI
import json
import base64
import os

class LLMParser(Parser):
    def __init__(self, filename):
        super().__init__(filename)
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    
    def _build_content(self, prompt):
        base64_images = self.get_data()

        content = [
            {
                "type": "text",
                "text":prompt
            },
        ]

        for img in base64_images:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img}"
                    }
                }
            )

        return content
       
    def parse(self, prompt):
        """Extract product name from image using OpenRouter"""
        try:
            # Encode image
            base64_image = self.get_data()
            
            # Call OpenRouter API
            response = self.client.chat.completions.create(
                model="qwen/qwen2.5-vl-72b-instruct:free",
                messages=[
                    {
                        "role": "user",
                        "content": self._build_content(prompt)
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=100
            )
            
            response = response.choices[0].message.content
            response = response.replace("'", "\"")  # Ensure valid JSON format
            response = json.loads(response)

            return response

            
        except Exception as e:
            print(f"Error parsing image: {e}")
            return None
