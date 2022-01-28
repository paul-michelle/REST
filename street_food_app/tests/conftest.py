import pytest


@pytest.fixture()
def generate_ticket(request):
    ticket = {
        "title": "DB Ticket",
        "description": "Ticket Description",
        "points": 1,
        "assigned_to": {
            "first_name": "Mr.A.N.Other",
            "github_account": "https://github.com/mr-a-n-other",
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
