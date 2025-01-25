from unittest import TestCase
from unittest.mock import patch, MagicMock
from golynx.infrastructure.database.supabase import SupabaseDatabase


class TestSupabase(TestCase):
    @patch("golynx.infrastructure.database.supabase.supabase")
    def setUp(self, mock_supabase):
        self.mock_client = MagicMock()
        mock_supabase.create_client.return_value = self.mock_client
        self.supabase = SupabaseDatabase()

    def test_supabase_client_initialization(self):
        self.assertEqual(self.supabase.client, self.mock_client)

    def test_get_returns_default_when_empty(self):
        mock_response = MagicMock()
        mock_response.data = []
        self.mock_client.table().select().eq().execute.return_value = mock_response

        result = self.supabase.get("nonexistent")
        self.assertEqual(result, self.supabase.default_redirection)

    def test_get_returns_golink_when_exists(self):
        mock_response = MagicMock()
        mock_response.data = [
            {
                "link": "test",
                "redirection": "http://test.com",
                "created_by": "test@test.com",
                "times_used": 0,
                "id": "123",
                "created_at": "2024-03-21",
            }
        ]
        self.mock_client.table().select().eq().execute.return_value = mock_response

        result = self.supabase.get("test")
        self.assertEqual(result.link, "test")
        self.assertEqual(result.redirection, "http://test.com")
