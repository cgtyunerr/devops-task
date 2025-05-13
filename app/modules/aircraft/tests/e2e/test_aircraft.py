"""E2e tests for aircraft."""

from tests import user_10000_token


class TestCreate:
    async def test_conflict(self, client):
        response = client.post(
            "/aircraft/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
            json={
                "manufacturer_serial_number": "4629",
                "type": "Airbus",
                "model": "Airbus A319-132",
                "operator_airline": "1",
                "number_of_engines": 2,
            },
        )

        assert response.status_code == 409


class TestGet:
    async def test_get_an_aircraft(self, client):
        response = client.get(
            "/aircraft/1/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
        )

        assert response.status_code == 200

    async def test_not_found(self, client):
        response = client.get(
            "/aircraft/3/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
        )

        assert response.status_code == 404


class TestUpdate:
    async def test_error_conflict_update(self, client):
        response = client.patch(
            "/aircraft/2/",
            headers={"Authorization": f"Bearer {user_10000_token}"},
            json={
                "manufacturer_serial_number": "4629",
                "type": "Airbus",
                "model": "Airbus A319-132",
                "operator_airline": "1",
                "number_of_engines": 2,
            },
        )

        assert response.status_code == 409
