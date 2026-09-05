import re
import sys


def fail_if_matches(agent_name, text, blocking_patterns):
    text = text or ""
    matches = []

    for pattern in blocking_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            matches.append(pattern)

    if matches:
        print(f"{agent_name} found blocking condition(s):")
        for match in matches:
            print(f"- {match}")
        print("Pipeline failed by AI agent gate.")
        sys.exit(1)

    print(f"{agent_name} gate passed.")


def fail(message):
    print(message)
    print("Pipeline failed by AI agent gate.")
    sys.exit(1)