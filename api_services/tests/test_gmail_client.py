import unittest
from unittest.mock import patch, MagicMock, mock_open
from api_services.api_calls.gmail_client import GoogleSheetsClient  # Adjust the import based on your project structure
import base64
from email.mime.text import MIMEText

class TestGoogleSheetsClient(unittest.TestCase):
    
    @patch('gmail_client.create_service')  # Ensure this path matches your import structure
    def setUp(self, mock_create_service):
        self.mock_service = MagicMock()
        mock_create_service.return_value = self.mock_service
        self.client = GoogleSheetsClient(client_secret_file='client_secret.json', scopes=['https://www.googleapis.com/auth/gmail.send'])

    def test_send_email_success(self):
        sender = "test@example.com"
        to = "recipient@example.com"
        subject = "Test Subject"
        message_text = "Test email body."
        mock_response = {'id': '12345', 'threadId': '67890'}

        self.mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = mock_response

        result = self.client.send_email(sender, to, subject, message_text)

        self.assertEqual(result, mock_response)

    def test_send_email_failure(self):
        sender = "test@example.com"
        to = "recipient@example.com"
        subject = "Test Subject"
        message_text = "Test email body."

        self.mock_service.users.return_value.messages.return_value.send.return_value.execute.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError):
            self.client.send_email(sender, to, subject, message_text)

    def test_list_emails_success(self):
        mock_response = {'messages': [{'id': '12345', 'threadId': '67890'}]}

        self.mock_service.users.return_value.messages.return_value.list.return_value.execute.return_value = mock_response

        result = self.client.list_emails()

        self.assertEqual(result, mock_response['messages'])

    def test_list_emails_failure(self):
        self.mock_service.users.return_value.messages.return_value.list.return_value.execute.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError):
            self.client.list_emails()

    def test_get_email_success(self):
        message_id = '12345'
        mock_response = {'id': message_id, 'threadId': '67890'}

        self.mock_service.users.return_value.messages.return_value.get.return_value.execute.return_value = mock_response

        result = self.client.get_email(message_id=message_id)

        self.assertEqual(result, mock_response)

    def test_get_email_failure(self):
        message_id = '12345'
        self.mock_service.users.return_value.messages.return_value.get.return_value.execute.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError):
            self.client.get_email(message_id=message_id)

    def test_search_emails_success(self):
        query = "subject:Test"
        mock_response = {'messages': [{'id': '12345', 'threadId': '67890'}]}

        self.mock_service.users.return_value.messages.return_value.list.return_value.execute.return_value = mock_response

        result = self.client.search_emails(query=query)

        self.assertEqual(result, mock_response)

    def test_search_emails_failure(self):
        self.mock_service.users.return_value.messages.return_value.list.return_value.execute.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError):
            self.client.search_emails()

    def test_create_message(self):
        sender = "test@example.com"
        to = "recipient@example.com"
        subject = "Test Subject"
        message_text = "Test email body."

        # Create the expected message using the same logic as in the method
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        expected_raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        result = self.client.create_message(sender, to, subject, message_text)

        # Check if the raw message generated by create_message matches the expected raw
        self.assertEqual(result['raw'], expected_raw)

    @patch("builtins.open", new_callable=mock_open, read_data="file content")
    def test_send_message_with_attachment_success(self, mock_file):
        to = "recipient@example.com"
        sender = "test@example.com"
        subject = "Test Subject"
        message_text = "Test email body."
        file_path = "dummy_path.txt"  # This will be mocked

        mock_response = {'id': '12345', 'threadId': '67890'}
        self.mock_service.users.return_value.messages.return_value.send.return_value.execute.return_value = mock_response

        result = self.client.send_message_with_attachment(to, sender, subject, message_text, file_path)

        self.assertEqual(result, mock_response)
        # Check if the specific file was opened
        open_calls = [call for call in mock_file.call_args_list if call[0][0] == file_path]
        self.assertEqual(len(open_calls), 1)  # Should have been called exactly once with the right file path

    def test_send_message_with_attachment_failure(self):
        to = "recipient@example.com"
        sender = "test@example.com"
        subject = "Test Subject"
        message_text = "Test email body."
        file_path = "dummy_path.txt"

        with patch("builtins.open", side_effect=Exception("File not found")):
            with self.assertRaises(RuntimeError):
                self.client.send_message_with_attachment(to, sender, subject, message_text, file_path)


if __name__ == '__main__':
    unittest.main()
