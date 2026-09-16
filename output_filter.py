import re
from typing import List, Tuple

class OutputFilter:
    """Фильтрация ответов LLM на наличие конфиденциальной информации."""



    PATTERNS = {
        'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        'password': re.compile(
            r'(?i)(?:password|passwd|pwd|пароль|пароля|паролем|пароли)\s*[:=]\s*\S+'
        ),
        'api_key': re.compile(
            r'(?i)(?:api[_-]?key|apikey|token|secret|api[_-]?ключ|токен|секрет)\s*[:=]\s*\S+'
        ),
    } 

    def __init__(self, patterns: dict = None):
        self.patterns = patterns if patterns is not None else self.PATTERNS.copy()

    def scan(self, text: str) -> List[Tuple[str, str]]:
        if not text:
            return []
        findings = []
        for data_type, pattern in self.patterns.items():
            for match in pattern.finditer(text):
                findings.append((data_type, match.group()))
        return findings

    def filter(self, text: str, replacement: str = '[REDACTED]') -> str:
        if not text:
            return text
        result = text
        for pattern in self.patterns.values():
            result = pattern.sub(replacement, result)
        return result

    def is_safe(self, text: str) -> bool:
        return len(self.scan(text)) == 0