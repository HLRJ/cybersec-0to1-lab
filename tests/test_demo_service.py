import pytest

from scripts.demo_service import build_event, validate_bind_host


@pytest.mark.parametrize("host", ["127.0.0.1", "192.168.77.1", "192.168.77.10"])
def test_validate_bind_host_allows_only_lab_addresses(host: str) -> None:
    assert validate_bind_host(host) == host


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.0.71", "8.8.8.8"])
def test_validate_bind_host_rejects_non_lab_addresses(host: str) -> None:
    with pytest.raises(ValueError, match="outside lab scope"):
        validate_bind_host(host)


def test_build_event_has_correlation_fields() -> None:
    event = build_event(
        client_ip="192.168.77.10",
        method="GET",
        path="/health",
        status=200,
        request_id="req-123",
        user_agent="curl/test",
    )
    assert event["request_id"] == "req-123"
    assert event["client_ip"] == "192.168.77.10"
    assert event["path"] == "/health"
    assert event["status"] == 200
    assert "+00:00" in event["timestamp"]