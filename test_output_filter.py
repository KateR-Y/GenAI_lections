import unittest
from output_filter import OutputFilter

class TestOutputFilter(unittest.TestCase):

    def setUp(self):
        self.filter = OutputFilter()

    def test_scan_email(self):
        text = "My email is test@example.com and also test2@domain.org"
        findings = self.filter.scan(text)
        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0][0], 'email')
        self.assertEqual(findings[0][1], 'test@example.com')

    def test_filter_password_and_api(self):
        text = "password: secret123, api_key: abc123"
        filtered = self.filter.filter(text)
        self.assertNotIn('secret123', filtered)
        self.assertNotIn('abc123', filtered)
        self.assertIn('[REDACTED]', filtered)

    def test_is_safe(self):
        safe_text = "Hello, how are you?"
        unsafe_text = "My email is user@mail.com"
        self.assertTrue(self.filter.is_safe(safe_text))
        self.assertFalse(self.filter.is_safe(unsafe_text))

    def test_scan_russian_password(self):
        """Проверяет, что фильтр находит русскоязычные пароли."""
        text = "Ваш пароль: secret123, а API-ключ: abc456"
        findings = self.filter.scan(text)
        types = [f[0] for f in findings]
        self.assertIn('password', types)
        self.assertIn('api_key', types)

if __name__ == '__main__':
    unittest.main()