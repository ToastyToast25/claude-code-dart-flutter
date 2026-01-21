#!/usr/bin/env python3
"""
Hook: Scan Dart files for security vulnerabilities
Checks for hardcoded secrets, injection patterns, insecure practices

Exit codes:
  0 = No issues
  1 = Warnings found (non-blocking)
  2 = Critical issues found (blocking)
"""

import json
import sys
import re

# Critical patterns that should block (exit code 2)
CRITICAL_PATTERNS = [
    # Hardcoded API keys and secrets
    (r'["\']sk[-_]live[-_][a-zA-Z0-9]{20,}["\']', 'Hardcoded Stripe live key'),
    (r'["\']pk[-_]live[-_][a-zA-Z0-9]{20,}["\']', 'Hardcoded Stripe publishable key'),
    (r'["\']AIza[a-zA-Z0-9_-]{35}["\']', 'Hardcoded Google API key'),
    (r'["\']ghp_[a-zA-Z0-9]{36}["\']', 'Hardcoded GitHub token'),
    (r'["\']gho_[a-zA-Z0-9]{36}["\']', 'Hardcoded GitHub OAuth token'),
    (r'["\']xox[baprs]-[a-zA-Z0-9-]{10,}["\']', 'Hardcoded Slack token'),
    (r'AKIA[A-Z0-9]{16}', 'Hardcoded AWS access key'),
    (r'["\'][a-f0-9]{32}["\'].*(?:api|key|secret|token)', 'Possible hardcoded secret'),

    # Firebase/Google credentials
    (r'["\']1:[0-9]+:android:[a-f0-9]+["\']', 'Hardcoded Firebase app ID'),

    # Private keys
    (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'Embedded private key'),
    (r'-----BEGIN CERTIFICATE-----', 'Embedded certificate'),
]

# Warning patterns (exit code 1)
WARNING_PATTERNS = [
    # SQL injection risks
    (r'\$\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE|DROP)', 'Potential SQL injection - use parameterized queries'),
    (r'["\'].*\s+(?:SELECT|INSERT|UPDATE|DELETE)\s+.*\$', 'SQL with string interpolation'),
    (r'query\s*\(\s*["\'].*\$\{', 'Raw query with interpolation'),

    # Command injection
    (r'Process\.run\s*\([^)]*\$', 'Process.run with interpolation - use list arguments'),
    (r'Process\.start\s*\([^)]*\$', 'Process.start with interpolation'),
    (r'shell:\s*true', 'Shell execution enabled - potential command injection'),

    # Insecure practices
    (r'http://', 'Insecure HTTP URL (use HTTPS)'),
    (r'verify\s*:\s*false', 'SSL verification disabled'),
    (r'allowInsecure\s*:\s*true', 'Insecure connection allowed'),
    (r'debugPrint\s*\(.*(?:password|secret|token|key)', 'Sensitive data in debug output'),
    (r'print\s*\(.*(?:password|secret|token|key)', 'Sensitive data in print'),
    (r'log\s*\(.*(?:password|secret|token|key)', 'Sensitive data in logs'),

    # Path traversal
    (r'File\s*\([^)]*\$\{', 'File path with interpolation - validate path'),
    (r'Directory\s*\([^)]*\$\{', 'Directory path with interpolation'),

    # XSS in web contexts
    (r'innerHTML\s*=', 'Direct innerHTML assignment - sanitize first'),
    (r'dangerouslySetInnerHTML', 'Dangerous HTML injection'),

    # Weak crypto
    (r'MD5\s*\(', 'MD5 is cryptographically weak'),
    (r'SHA1\s*\(', 'SHA1 is deprecated for security'),

    # Hardcoded credentials (less certain)
    (r'password\s*[=:]\s*["\'][^"\']+["\']', 'Possible hardcoded password'),
    (r'secret\s*[=:]\s*["\'][^"\']+["\']', 'Possible hardcoded secret'),
]

# Patterns to ignore (false positive reducers)
IGNORE_PATTERNS = [
    r'//\s*ignore:',  # Explicit ignore comments
    r'test/',  # Test files often have test credentials
    r'_test\.dart',
    r'mock',
    r'example',
    r'\.env\.example',
]


def should_ignore(content: str, file_path: str) -> bool:
    """Check if file/content should be ignored."""
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True
    return False


def scan_content(content: str, file_path: str) -> tuple:
    """Scan content for security issues. Returns (critical, warnings)."""
    if should_ignore(content, file_path):
        return [], []

    critical = []
    warnings = []

    # Check critical patterns
    for pattern, message in CRITICAL_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            critical.append(message)

    # Check warning patterns
    for pattern, message in WARNING_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            # Skip http:// in comments or specific allowed cases
            if 'http://' in pattern:
                # Allow http://localhost, http://127.0.0.1
                if re.search(r'http://(localhost|127\.0\.0\.1|10\.|192\.168\.)', content):
                    continue
            warnings.append(message)

    return critical, warnings


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    new_content = tool_input.get('new_string', '') or tool_input.get('content', '')

    # Only scan Dart files
    if not file_path.endswith('.dart'):
        sys.exit(0)

    if not new_content:
        sys.exit(0)

    critical, warnings = scan_content(new_content, file_path)

    # Remove duplicates
    critical = list(set(critical))
    warnings = list(set(warnings))

    if critical:
        response = {
            "feedback": f"SECURITY CRITICAL: {', '.join(critical[:3])}",
            "block": True
        }
        print(json.dumps(response))
        sys.exit(2)

    if warnings:
        response = {
            "feedback": f"Security warnings: {', '.join(warnings[:3])}"
        }
        print(json.dumps(response))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
