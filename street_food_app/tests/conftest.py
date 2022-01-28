import os
import pytest


@pytest.fixture(autouse=False)
def generate_sample_ticket(request):
    ticket = {
        "title": "DB Ticket",
        "description": "Ticket Description",
        "points": 1,
        "assigned_to": {
            "first_name": "A.N.Other",
            "github_account": f"https://github.com/",
            "stack": [
                {
                    "language_name": "C++",
                    "experience": 3.5,
                    "description": "Strong Knowledge"
                }
            ],
            "hobbies": [
                "Swimming", "Skiing"
            ]
        }
    }
    yield ticket


@pytest.fixture(autouse=False)
def roll_back_transaction(request):
    os.system('python manage.py flush_tickets')
