import json
from django.test import TestCase, override_settings
from apps.arrivals.models import Arrival

VALID_PAYLOAD = {
    "latitude": -2.1812473,
    "longitude": -79.8146685,
    "device_id": "test-device",
}


@override_settings(TRACKER_API_KEY="secret-test-key")
class ArrivalCreateTest(TestCase):

    def _post(self, payload=None, key="secret-test-key"):
        headers = {"HTTP_X_API_KEY": key} if key else {}
        return self.client.post(
            "/api/arrivals/",
            data=json.dumps(payload or VALID_PAYLOAD),
            content_type="application/json",
            **headers,
        )

    def test_valid_key_creates_record(self):
        response = self._post()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Arrival.objects.count(), 1)
        arrival = Arrival.objects.first()
        self.assertAlmostEqual(arrival.latitude, -2.1812473)
        self.assertEqual(arrival.device_id, "test-device")

    def test_wrong_key_returns_403(self):
        response = self._post(key="wrong-key")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Arrival.objects.count(), 0)

    def test_missing_key_returns_403(self):
        response = self._post(key=None)
        self.assertEqual(response.status_code, 403)

    def test_missing_latitude_returns_400(self):
        response = self._post(payload={"longitude": -79.81, "device_id": "x"})
        self.assertEqual(response.status_code, 400)

    def test_missing_longitude_returns_400(self):
        response = self._post(payload={"latitude": -2.18, "device_id": "x"})
        self.assertEqual(response.status_code, 400)

    def test_device_id_is_optional(self):
        response = self._post(payload={"latitude": -2.18, "longitude": -79.81})
        self.assertEqual(response.status_code, 201)


@override_settings(TRACKER_API_KEY="")
class ArrivalOpenEndpointTest(TestCase):

    def test_post_without_key_when_api_key_empty(self):
        response = self.client.post(
            "/api/arrivals/",
            data=json.dumps(VALID_PAYLOAD),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)


class ArrivalListTest(TestCase):

    def setUp(self):
        Arrival.objects.create(latitude=-2.18, longitude=-79.81, device_id="dev-1")
        Arrival.objects.create(latitude=-2.19, longitude=-79.82, device_id="dev-2")

    def test_get_returns_200(self):
        response = self.client.get("/api/arrivals/")
        self.assertEqual(response.status_code, 200)

    def test_get_returns_all_records(self):
        response = self.client.get("/api/arrivals/")
        self.assertEqual(len(response.json()), 2)

    def test_get_does_not_require_api_key(self):
        response = self.client.get("/api/arrivals/")
        self.assertEqual(response.status_code, 200)
