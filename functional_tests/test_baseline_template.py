from selenium.webdriver.common.by import By
from .base import BaseFunctionalTest
from street_food_app.views import ticket_list_or_create_next
from street_food_app.models import DEFAULT_TICKET_TITLE, DEFAULT_TICKET_DESCRIPTION
from django.urls import reverse

NOTHING_SEND = ""
BLANK_TICKET_TITLE = '{"title": ""}'
BLANK_FIELD_ERROR = "This field may not be blank."
NON_BLANK_TICKET_TITLE = '{"title": "A ticket for back-end"}'
ANOTHER_NON_BLANK_TICKET_TITLE = '{"title": "Another ticket for back-end"}'


class InitialTest(BaseFunctionalTest):

    def test_can_create_a_ticket_with_default_values(self):
        self.browser.get(self.live_server_url + reverse(ticket_list_or_create_next))
        self.assertIn('Ticket List Or Create Next', self.browser.title)
        self.assertNotIn(DEFAULT_TICKET_TITLE, self.browser.find_element(By.CLASS_NAME, 'response-info').text)
        self.assertNotIn(DEFAULT_TICKET_DESCRIPTION, self.browser.find_element(By.CLASS_NAME, 'response-info').text)

        self.send_info(NOTHING_SEND)

        self.wait_and_assert_is_in_response(DEFAULT_TICKET_TITLE)
        self.wait_and_assert_is_in_response(DEFAULT_TICKET_DESCRIPTION)

    def test_returns_specific_error_when_malformed_response(self):
        self.browser.get(self.live_server_url + reverse(ticket_list_or_create_next))
        self.assertNotIn(BLANK_FIELD_ERROR, self.browser.find_element(By.CLASS_NAME, 'response-info').text)

        self.send_info(BLANK_TICKET_TITLE)

        self.wait_and_assert_is_in_response(BLANK_FIELD_ERROR)

    def test_can_create_and_then_receive_all_tickets_from_db_if_valid_info(self):
        self.browser.get(self.live_server_url + reverse(ticket_list_or_create_next))

        self.send_info(NON_BLANK_TICKET_TITLE)
        self.wait_for(lambda: self.send_info(ANOTHER_NON_BLANK_TICKET_TITLE))

        self.browser.get(self.live_server_url + reverse(ticket_list_or_create_next))
        self.wait_and_assert_is_in_response("A ticket for back-end")
        self.wait_and_assert_is_in_response("Another ticket for back-end")
