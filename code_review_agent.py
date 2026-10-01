

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

```text
In your code-review-agent.py, the large prompt = f"""...""" section is the prompt that you send to the LLM.
But there is an important distinction:
code-review-agent.py is the Agent. The prompt is the instructions given to the LLM.
```

```text
I have this project , please explain in simple beginner friendly way in terms of GenAI ,AgenticAI,RAG 
 AI Agent in CI/CD

Our ultimate architecture is:

Developer
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Code Review Agent
    ↓
Security Agent
    ↓
Deployment Risk Agent
    ↓
Deployment
    ↓
Health Check
    ↓
Log Analysis Agent

This is where AI becomes useful in DevOps.

Yes. Let's connect your AI Agent in CI/CD project to the three concepts—GenAI, Agentic AI, and RAG—in a very beginner-friendly way.

Your architecture is:
Developer
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Code Review Agent
    ↓
Security Agent
    ↓
Deployment Risk Agent
    ↓
Deployment
    ↓
Health Check
    ↓
Log Analysis Agent

The easiest way to understand it is:

    GenAI is the brain, RAG is the knowledge source, and Agentic AI is the worker that uses the brain and tools to perform a task.

1. First: What is GenAI?

Generative AI means AI that can generate new content based on a prompt.

For example, you give an LLM:
Review this Python code:

@app.route("/")
def home():
    return "Hello"

The AI might respond:
The code is valid, but consider adding error handling
and avoiding debug mode in production.

That's GenAI.

Examples of GenAI models you have worked with include:
Gemini
Groq-hosted models
GPT models

The model itself is basically:
Input
  ↓
LLM
  ↓
Generated response

At this stage, it's just AI answering a question.
```

```text
2. Then what is an AI Agent?

An AI Agent is more than just asking an LLM a question.

An agent has:
Goal
 ↓
Reasoning
 ↓
Tools
 ↓
Actions
 ↓
Result

For example:
Goal:
"Check whether this code is safe to deploy."

        ↓

Agent examines code

        ↓

Uses tools
 ├── Git diff
 ├── Security scanner
 └── LLM

        ↓

Makes decision

        ↓

PASS / FAIL

So:

    LLM = brain

while:

    Agent = brain + instructions + tools + ability to take actions

This is the important difference.
```

```text

3. Your Code Review Agent

Let's take your first agent.
GitHub
   ↓
Code Review Agent

Suppose a developer commits:
app.run(
    host="0.0.0.0",
    debug=True
)

Your Code Review Agent can inspect the changed code and ask the LLM:
Review this code for:
- bugs
- bad practices
- production issues
- maintainability

The LLM might identify:
Risk:
debug=True is enabled.

Recommendation:
Disable debug mode in production.

Here:
Code Review Agent
      |
      ├── Gets Git diff
      |
      ├── Sends relevant code to LLM
      |
      ├── LLM analyzes it
      |
      └── Agent produces result

That's GenAI being used inside an agent.

```

```text
4. Where does RAG come into this?

This is where things become interesting.

Imagine your company has security rules:
Company Security Policy

1. Never hardcode passwords.
2. Never expose AWS access keys.
3. Production containers must run as non-root.
4. Debug mode must be disabled.
5. Images must come from approved registries.

If you simply ask an LLM:
Is this code secure?

the model relies mostly on its general knowledge.

But what if you give it your company's actual policies?

That's where RAG comes in.
```

```text

5. RAG in simple terms

RAG = Retrieval-Augmented Generation

Break the name apart:
Retrieval
    +
Augmented
    +
Generation

Meaning:

    Retrieve relevant information first, then give that information to the GenAI model so it can generate a better answer.

For example:
Developer code
      ↓
Find relevant company security policies
      ↓
Relevant policy:
"debug=True is prohibited in production"
      ↓
LLM
      ↓
Analysis

So:
RAG
=
Your knowledge
+
LLM

```

```text
6. Imagine your company has 1,000 documents

For example:
Company Documentation
│
├── Security Policies
├── Kubernetes Standards
├── AWS Standards
├── Azure Standards
├── Coding Guidelines
├── Deployment Procedures
└── Incident Runbooks

You don't want to send all 1,000 documents to the LLM every time.

Instead, RAG does:
Question:
"Is this Kubernetes deployment secure?"

             ↓

       RAG Retrieval
             ↓
Find relevant documents
             ↓

Kubernetes Security Standard
Container Security Policy
RBAC Guidelines

             ↓

            LLM
             ↓

       Generated answer

That's RAG.

```
```text
7. Now connect RAG to your Security Agent

Your architecture becomes:
Developer
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Security Agent
    ↓
RAG
    ↓
Company Security Policies
    ↓
LLM
    ↓
Security Decision

For example, developer commits:

containers:
- name: app
  securityContext:
    privileged: true

The Security Agent retrieves:
Company Kubernetes Security Policy:

"Privileged containers are prohibited."

Then gives both to the LLM:
Code:
privileged: true

Policy:
Privileged containers are prohibited.

Question:
Does this deployment violate company policy?

LLM:
YES

Reason:
The deployment enables privileged mode,
which violates the company Kubernetes security policy.

Now your agent can cause the pipeline to stop.
```

```text

8. Your Deployment Risk Agent

Now let's look at:
Security Agent
      ↓
Deployment Risk Agent

This agent asks:

    "If we deploy this change, what could go wrong?"

Suppose the developer changes:
database connection code

The Deployment Risk Agent might examine:
Git diff
+
Application configuration
+
Previous deployment information
+
Known incidents
+
Company deployment rules

Then the LLM analyzes it.

For example:
Risk level: HIGH

Reason:
Database connection logic was modified.
This affects a critical production component.
Additional validation is recommended.

Again:
Agent
  ↓
Collect information
  ↓
RAG / tools
  ↓
LLM
  ↓
Decision
```

```text

9. Then comes Deployment

If the agents pass the checks:
Code Review Agent
       ↓
     PASS
       ↓
Security Agent
       ↓
     PASS
       ↓
Deployment Risk Agent
       ↓
     PASS
       ↓
Deployment

GitHub Actions is the orchestrator here.

It controls the workflow.

For example:

jobs:

  code-review:
      ...

  security:
      needs: code-review

  deployment-risk:
      needs: security

  deploy:
      needs: deployment-risk

So GitHub Actions says:

    "Run this agent first. If it passes, run the next one."
```
```text

10. Then Health Check

After deployment:
Deployment
    ↓
Health Check

For example:

curl https://myapp.example.com/health

Expected:

{
  "status": "ok"
}

If health check fails:
Deployment
    ↓
Health Check
    ↓
FAILED
```
```text


Now we can involve another AI Agent.
11. Log Analysis Agent

This is where your architecture becomes very powerful.

Suppose deployment succeeded but logs contain:
ERROR: Database connection timeout
ERROR: Connection refused
ERROR: Failed to initialize application

Normally a DevOps engineer would:
Open logs
    ↓
Read errors
    ↓
Search documentation
    ↓
Check configuration
    ↓
Investigate

Your Log Analysis Agent can help automate that.
Application logs
      ↓
Log Analysis Agent
      ↓
Relevant logs extracted
      ↓
RAG
      ↓
Runbooks / documentation
      ↓
LLM
      ↓
Analysis

It might produce:
Probable cause:
Application cannot connect to the database.

Evidence:
Connection timeout appears repeatedly.

Recommended checks:
1. Verify DB endpoint.
2. Verify network connectivity.
3. Verify security group rules.
4. Verify database credentials.
12. The complete architecture

Now we can put everything together.
                       ┌───────────────┐
                       │   Developer   │
                       └───────┬───────┘
                               ↓
                       ┌───────────────┐
                       │    GitHub     │
                       └───────┬───────┘
                               ↓
                       ┌───────────────┐
                       │ GitHub Actions│
                       └───────┬───────┘
                               ↓
                    ┌─────────────────────┐
                    │ Code Review Agent   │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Security Agent     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Deployment Risk     │
                    │ Agent               │
                    └──────────┬──────────┘
                               ↓
                         ┌──────────┐
                         │ Deploy   │
                         └────┬─────┘
                              ↓
                       ┌────────────┐
                       │Health Check│
                       └─────┬──────┘
                             ↓
                    ┌──────────────────┐
                    │ Log Analysis     │
                    │ Agent             │
                    └────────┬─────────┘
                             ↓
                          Result

And underneath the agents:
                 ┌─────────────────┐
                 │      RAG        │
                 │                 │
                 │ Company docs    │
                 │ Policies        │
                 │ Runbooks        │
                 │ Standards       │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │      LLM        │
                 │ Gemini / GPT /  │
                 │ other models    │
                 └─────────────────┘
```
```text
                 
13. The easiest way to remember the three concepts

Think of a DevOps engineer.
GenAI = Brain
"Analyze this code."

The LLM generates an answer.
RAG = Knowledge library
"Here are our company's policies,
runbooks and standards."

The AI gets organization-specific information.
Agentic AI = DevOps engineer
I have a goal.

I'll:
1. inspect the code
2. retrieve relevant policies
3. ask the LLM
4. make a decision
5. run tools
6. report the result

So:
             AI-powered CI/CD

                   Agent
                     │
          ┌──────────┴──────────┐
          │                     │
        Tools                  RAG
          │                     │
   GitHub / logs /        Company knowledge
   scanners / APIs              │
          │                     │
          └──────────┬──────────┘
                     ↓
                    LLM
                 (GenAI)
                     ↓
                  Decision
                     ↓
              Pipeline action
```              
```text
              
14. In your particular project

You already have a very good structure for demonstrating this:
Component	AI concept
Gemini/Groq model	GenAI / LLM
Code Review Agent	Agentic AI
Security Agent	Agentic AI
Deployment Risk Agent	Agentic AI
Log Analysis Agent	Agentic AI
Company policies/docs	RAG knowledge base
Retrieval of relevant policies	RAG
GitHub Actions	CI/CD orchestrator
GitHub	Source control
Deployment	DevOps action
Health check	Operational validation

The important thing is that you don't need RAG for every agent.

For example:
Code Review Agent
      ↓
LLM

can be useful without RAG.

But:
Security Agent
      ↓
Company security policies
      ↓
RAG
      ↓
LLM

becomes much more organization-specific.

And the most complete architecture is:

    GitHub Actions orchestrates the workflow → Agents perform specialized tasks → RAG supplies organization-specific knowledge → GenAI/LLM provides reasoning and generation → Agents use tools to take or recommend actions.

That is the core idea behind bringing Agentic AI into CI/CD.
```

