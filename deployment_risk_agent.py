from ai_provider import ask_ai

print("Running Deployment Risk Agent...")

prompt = """
Analyze deployment risks for this application.

Evaluate:
- Deployment stability risks
- Dependency risks
- Production readiness risks
- Downtime risks
- Scalability concerns
- Rollback considerations

Provide:

Risk Level:
LOW / MEDIUM / HIGH

Findings:
- ...

Recommendations:
- ...

Important:
- This is an advisory analysis only.
- Do NOT recommend blocking deployment.
- Do NOT return PASS or FAIL.
- Do NOT recommend rollback unless there is clear evidence.
"""

response = ask_ai(prompt)

print("\n===== Deployment Risk Report =====")
print(response)
print("==================================")

print("Deployment Risk Agent completed successfully.")