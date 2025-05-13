"""E2e test for user api."""


class TestRegister:
    async def test_conflict(self, client):
        response = client.post(
            "/user/register/",
            json={
                "username": "deneme",
                "password": "password",
            },
        )

        assert response.status_code == 409
