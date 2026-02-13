import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_check_returns_200(api_client: APIClient) -> None:
    url = reverse("health-check")
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data["status"] == "healthy"
