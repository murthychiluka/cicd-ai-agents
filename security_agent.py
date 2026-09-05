import os
import re

from agent_guard import fail


print("Running Security Agent...")


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SCAN_EXTENSIONS = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".yml",
    ".yaml",
    ".env",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".github",
    "node_modules",
}


# --------------------------------------------------
# Security patterns
# --------------------------------------------------

SECURITY_PATTERNS = {
    "Password": r"password\s*[:=]\s*['\"][^'\"]+['\"]",

    "Secret": r"secret\s*[:=]\s*['\"][^'\"]+['\"]",

    "API Key": r"(api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]",

    "Token": r"(token|access[_-]?token)\s*[:=]\s*['\"][^'\"]+['\"]",

    "AWS Access Key": r"\bAKIA[0-9A-Z]{16}\b",

    "Private Key": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
}


# --------------------------------------------------
# Scan repository
# --------------------------------------------------

findings = []


for root, directories, files in os.walk("."):

    # Prevent scanning excluded directories
    directories[:] = [
        directory
        for directory in directories
        if directory not in EXCLUDED_DIRECTORIES
    ]

    for filename in files:

        extension = os.path.splitext(filename)[1].lower()

        if extension not in SCAN_EXTENSIONS:
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(file, start=1):

                    for issue_type, pattern in SECURITY_PATTERNS.items():

                        if re.search(
                            pattern,
                            line,
                            flags=re.IGNORECASE
                        ):

                            findings.append({
                                "file": filepath,
                                "line": line_number,
                                "type": issue_type,
                                "content": line.strip(),
                            })

        except Exception as error:

            print(
                f"Warning: Could not scan {filepath}: {error}"
            )


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n========== SECURITY SCAN ==========")


if findings:

    print(
        f"Security Agent found {len(findings)} "
        f"potential security issue(s).\n"
    )

    for finding in findings:

        print(f"File     : {finding['file']}")
        print(f"Line     : {finding['line']}")
        print(f"Type     : {finding['type']}")
        print(f"Content  : {finding['content']}")
        print("-----------------------------------")


    print("===================================")

    fail(
        "Security Agent detected potential "
        "hardcoded secrets or sensitive information."
    )


print("No potential hardcoded secrets detected.")

print("===================================")

print("Security Agent gate passed.")