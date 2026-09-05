from ai_provider import ask_ai


prompt = """
You are testing an AI provider layer.

Reply with exactly:
AI PROVIDER TEST SUCCESS
"""

response = ask_ai(prompt)

print("\n===== AI RESPONSE =====")
print(response)
print("======================")