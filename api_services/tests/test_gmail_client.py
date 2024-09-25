import unittest
from unittest.mock import MagicMock, patch
from api_services.api_calls.gmail_client import GoogleSheetsClient

class TestGoogleGmailClient(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        self.gmail_client = GoogleSheetsClient(client_secret_file="fake_secret.json")
        self.gmail_client.service = self.mock_service

    @patch("google_services.gmail_client.create_service")
    def test_send_email_success(self, mock_create_service):
        self.mock_service.users().messages().send.return_value.execute.return_value = {"id": "message_id"}
        result = self.gmail_client.send_email("sender@example.com", "recipient@example.com", "Test Subject", "Test message")
        self.mock_service.users().messages().send.assert_has_calls([
            unittest.mock.call(userId="me", body={"raw": unittest.mock.ANY}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["id"], "message_id")

    @patch("google_services.gmail_client.create_service")
    def test_list_emails_success(self, mock_create_service):
        self.mock_service.users().messages().list.return_value.execute.return_value = {"messages": [{"id": "message_id"}]}
        result = self.gmail_client.list_emails(max_results=5)
        self.mock_service.users().messages().list.assert_has_calls([
            unittest.mock.call(userId="me", maxResults=5),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result[0]["id"], "message_id")

    @patch("google_services.gmail_client.create_service")
    def test_get_email_success(self, mock_create_service):
        self.mock_service.users().messages().get.return_value.execute.return_value = {"id": "message_id"}
        result = self.gmail_client.get_email(message_id="message_id")
        self.mock_service.users().messages().get.assert_has_calls([
            unittest.mock.call(userId="me", id="message_id"),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["id"], "message_id")

    @patch("google_services.gmail_client.create_service")
    def test_search_emails_success(self, mock_create_service):
        self.mock_service.users().messages().list.return_value.execute.return_value = {"messages": [{"id": "message_id"}]}
        result = self.gmail_client.search_emails(query="subject:test")
        self.mock_service.users().messages().list.assert_has_calls([
            unittest.mock.call(userId="me", q="subject:test", maxResults=10),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["messages"][0]["id"], "message_id")

    @patch("google_services.gmail_client.create_service")
    def test_send_message_with_attachment(self, mock_create_service):
        self.mock_service.users().messages().send.return_value.execute.return_value = {"id": "message_id"}
        result = self.gmail_client.send_message_with_attachment("recipient@example.com", "sender@example.com", "Test Subject", "Test message", "fake_path.txt")
        self.mock_service.users().messages().send.assert_has_calls([
            unittest.mock.call(userId="me", body={"raw": unittest.mock.ANY}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["id"], "message_id")

    @patch("google_services.gmail_client.create_service")
    def test_send_email_fail(self, mock_create_service):
        self.mock_service.users().messages().send.side_effect = Exception("Failed to send email")
        with self.assertRaises(RuntimeError):
            self.gmail_client.send_email("sender@example.com", "recipient@example.com", "Test Subject", "Test message")

    @patch("google_services.gmail_client.create_service")
    def test_get_email_fail(self, mock_create_service):
        self.mock_service.users().messages().get.side_effect = Exception("Failed to get email")
        with self.assertRaises(RuntimeError):
            self.gmail_client.get_email(message_id="message_id")

if __name__ == "__main__":
    unittest.main()
