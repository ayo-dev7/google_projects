import unittest
from unittest.mock import MagicMock, patch
from api_services.api_calls.sheet_client import GoogleSheetsClient

class TestGoogleSheetsClient(unittest.TestCase):

    def setUp(self):
        # Mock the Google Sheets API service
        self.mock_service = MagicMock()
        self.sheet_client = GoogleSheetsClient(client_secret_file="fake_secret.json")
        self.sheet_client.service = self.mock_service

    @patch("google_services.sheet_client.create_service")
    def test_get_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().get.return_value.execute.return_value = {"spreadsheetId": "spreadsheet_id"}
        result = self.sheet_client.get_sheet("spreadsheet_id")
        self.mock_service.spreadsheets().get.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id"),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["spreadsheetId"], "spreadsheet_id")

    @patch("google_services.sheet_client.create_service")
    def test_read_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().values().get.return_value.execute.return_value = {"values": [["A1", "B1"]]}
        result = self.sheet_client.read_sheet("spreadsheet_id", "range_name")
        self.mock_service.spreadsheets().values().get.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", range="range_name"),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["values"], [["A1", "B1"]])

    @patch("google_services.sheet_client.create_service")
    def test_append_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().values().append.return_value.execute.return_value = {"updates": "success"}
        result = self.sheet_client.append_sheet("spreadsheet_id", "range_name", [["A1", "B1"]])
        self.mock_service.spreadsheets().values().append.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", range="range_name", valueInputOption="RAW", body={"values": [["A1", "B1"]]}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["updates"], "success")

    @patch("google_services.sheet_client.create_service")
    def test_update_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().values().update.return_value.execute.return_value = {"updatedRange": "Sheet1!A1:B1"}
        result = self.sheet_client.update_sheet("spreadsheet_id", "range_name", [["A1", "B1"]])
        self.mock_service.spreadsheets().values().update.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", range="range_name", valueInputOption="RAW", body={"values": [["A1", "B1"]]}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["updatedRange"], "Sheet1!A1:B1")

    @patch("google_services.sheet_client.create_service")
    def test_create_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().batchUpdate.return_value.execute.return_value = {"replies": [{"addSheet": {"properties": {"sheetId": "sheet_id"}}}]}
        result = self.sheet_client.create_sheet("spreadsheet_id", "Sheet1")
        self.mock_service.spreadsheets().batchUpdate.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", body={"requests": [{"addSheet": {"properties": {"title": "Sheet1"}}}]}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["replies"][0]["addSheet"]["properties"]["sheetId"], "sheet_id")

    @patch("google_services.sheet_client.create_service")
    def test_delete_sheet_success(self, mock_create_service):
        self.mock_service.spreadsheets().batchUpdate.return_value.execute.return_value = {"replies": [{"deleteSheet": {"sheetId": "sheet_id"}}]}
        result = self.sheet_client.delete_sheet("spreadsheet_id", "sheet_id")
        self.mock_service.spreadsheets().batchUpdate.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", body={"requests": [{"deleteSheet": {"sheetId": "sheet_id"}}]}),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["replies"][0]["deleteSheet"]["sheetId"], "sheet_id")

    @patch("google_services.sheet_client.create_service")
    def test_batch_update_success(self, mock_create_service):
        self.mock_service.spreadsheets().batchUpdate.return_value.execute.return_value = {"updated": "success"}
        body = {"requests": [{"updateCells": {}}]}
        result = self.sheet_client.batch_update("spreadsheet_id", body)
        self.mock_service.spreadsheets().batchUpdate.assert_has_calls([
            unittest.mock.call(spreadsheetId="spreadsheet_id", body=body),
            unittest.mock.call().execute()
        ])
        self.assertEqual(result["updated"], "success")

if __name__ == "__main__":
    unittest.main()
