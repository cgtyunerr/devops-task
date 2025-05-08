"""E2e test for main app."""


class TestGetHealth:
    async def test_200(self, client):
        result = client.get("/health/")

        assert result.status_code == 200
        assert result.json().get("message") == "OK"
