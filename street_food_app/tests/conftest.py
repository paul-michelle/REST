import pytest
from street_food_app.models import Developer


@pytest.fixture
def testing_ticket():
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
    return ticket


@pytest.fixture()
def sample_ticket(testing_ticket):
    sample_ticket = testing_ticket
    yield sample_ticket
    Developer.objects.all().delete()
