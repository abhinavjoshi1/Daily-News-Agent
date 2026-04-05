"""
Filename : test_email.py
Desciption : Test file for email sender logic.
"""

# --------------- Imports ---------------
from tools.email_sender import send_email
from datetime import datetime

subject = f"AI News Test - {datetime.now().strftime('%Y-%m-%d')}"

body = """
AI News (Test)

1. Example headline
- Summary point 1
- Summary point 2

2. Another news
- Insight 1
"""

send_email(body)
