"""E2e tests for airline."""

from tests import user_10000_token


class TestCreate:
    async def test_conflict(self, client):
        response = client.post(
            "/airline/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
            json={
                "name": "deneme",
                "callsign": "THY",
                "founded_year": "1856",
                "base_airport": "IST",
            },
        )

        assert response.status_code == 409


class TestGet:
    async def test_get_all(self, client):
        response = client.get(
            "/airline/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
        )

        assert response.status_code == 200

    async def test_get_an_airline(self, client):
        response = client.get(
            "/airline/1/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
        )

        assert response.status_code == 200

    async def test_not_found(self, client):
        response = client.get(
            "/airline/3/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
        )

        assert response.status_code == 404


class TestUpdate:
    async def test_error_conflict_update(self, client):
        response = client.patch(
            "/airline/2/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
            json={
                "name": "deneme",
                "callsign": "THY",
                "founded_year": "1856",
                "base_airport": "IST",
            },
        )

        assert response.status_code == 409
