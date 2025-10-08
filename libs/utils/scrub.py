
import re
SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    r"(?i)password\s*=\s*['\"][^'\" ]{6,}['\"]",
]
def scrub(text: str) -> str:
    out = text
    for p in SECRET_PATTERNS:
        out = re.sub(p, "[REDACTED]", out)
    return out
