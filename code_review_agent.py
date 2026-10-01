

from ai_provider import ask_ai
from agent_guard import fail_if_matches


print("Running AI Code Review Agent...")


# --------------------------------------------------
# Read application code
# --------------------------------------------------

try:
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()

except FileNotFoundError:
    print("ERROR: app.py not found.")
    raise


# --------------------------------------------------
# Build AI review prompt
# --------------------------------------------------

prompt = f"""
You are a senior Python and Flask code reviewer.

Review the following Flask application before production deployment.

Analyze the code for:

1. Security issues
   - hardcoded secrets
   - unsafe input handling
   - command injection
   - insecure configuration
   - exposed sensitive information

2. Code quality
   - bugs
   - poor coding practices
   - maintainability problems
   - unnecessary complexity

3. Performance
   - inefficient operations
   - blocking operations
   - resource usage concerns

4. Deployment risks
   - application startup problems
   - missing dependencies
   - configuration problems
   - production-readiness issues

5. Reliability
   - exception handling
   - failure scenarios
   - health-check concerns

IMPORTANT:

The AI review is a deployment gate.

Use PIPELINE_STATUS: FAIL ONLY when there is a
critical or high-risk issue that should block production deployment.

Use PIPELINE_STATUS: PASS when there are no
critical or high-risk issues.

Do not fail the pipeline for minor suggestions,
style issues, or low-risk improvements.

Return your review using this structure:

Summary:
<short summary>

Security:
- ...

Code Quality:
- ...

Performance:
- ...

Deployment Risks:
- ...

Recommendations:
- ...

Risk Level:
LOW / MEDIUM / HIGH / CRITICAL

PIPELINE_STATUS: PASS or FAIL

Here is the application code:

{code}
"""


# --------------------------------------------------
# Ask AI provider
# --------------------------------------------------

try:
    response = ask_ai(prompt)

except Exception as error:
    print(f"AI Code Review failed: {error}")
    raise


# --------------------------------------------------
# Display AI review
# --------------------------------------------------

print("\n========== AI CODE REVIEW ==========")
print(response)
print("====================================")


# --------------------------------------------------
# Deployment gate
# --------------------------------------------------

blocking_patterns = [
    r"risk\s*level\s*:\s*(high|critical)",
    r"severity\s*:\s*(high|critical)",
    r"\bdeployment should not proceed\b",
    r"\bdo not deploy\b",
    r"\bpipeline_status\s*:\s*fail\b",
]


fail_if_matches(
    "AI Code Review Agent",
    response,
    blocking_patterns
)

