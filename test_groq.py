
import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence."
        }
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)
