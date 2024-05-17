import logging
from unittest import mock
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from photobooth.application import app
from photobooth.container import container
from photobooth.services.config import appconfig
from photobooth.services.processingservice import ProcessingService
from photobooth.utils.exceptions import ProcessMachineOccupiedError

logger = logging.getLogger(name=None)


@pytest.fixture(autouse=True)
def run_around_tests():
    appconfig.reset_defaults()

    yield


@pytest.fixture
def client() -> TestClient:
    with TestClient(app=app, base_url="http://test/api/") as client:
        container.start()
        yield client
        container.stop()


def test_chose_1pic(client: TestClient):
    with patch.object(container.processing_service, "start_job_1pic"):
        # emulate action
        response = client.get("/processing/chose/1pic")
        assert response.status_code == 200

        container.processing_service.start_job_1pic.assert_called()


def test_chose_collage(client: TestClient):
    with patch.object(container.processing_service, "start_job_collage"):
        # emulate action
        response = client.get("/processing/chose/collage")
        assert response.status_code == 200

        container.processing_service.start_job_collage.assert_called()


def test_chose_animation(client: TestClient):
    with patch.object(container.processing_service, "start_job_animation"):
        # emulate action
        response = client.get("/processing/chose/animation")
        assert response.status_code == 200

        container.processing_service.start_job_animation.assert_called()


def test_chose_video(client: TestClient):
    with patch.object(container.processing_service, "start_or_stop_job_video"):
        # emulate action
        response = client.get("/processing/chose/video")
        assert response.status_code == 200

        container.processing_service.start_or_stop_job_video.assert_called()


def test_chose_video_stoprecording(client: TestClient):
    with patch.object(container.processing_service, "stop_recording"):
        # emulate action
        response = client.get("/processing/cmd/stop")
        assert response.status_code == 200

        container.processing_service.stop_recording.assert_called()


def test_chose_1pic_occupied(client: TestClient):
    error_mock = mock.MagicMock()
    error_mock.side_effect = ProcessMachineOccupiedError("mock error")

    with patch.object(ProcessingService, "start_job_1pic", error_mock):
        response = client.get("/processing/chose/1pic")
        assert response.status_code == 400


def test_chose_1pic_otherexception(client: TestClient):
    error_mock = mock.MagicMock()
    error_mock.side_effect = Exception("mock error")

    with patch.object(ProcessingService, "start_job_1pic", error_mock):
        response = client.get("/processing/chose/1pic")
        assert response.status_code == 500


def test_confirm_reject_abort(client: TestClient):
    with patch.object(container.processing_service, "confirm_capture"):
        # emulate action
        response = client.get("/processing/cmd/confirm")
        assert response.status_code == 200

        container.processing_service.confirm_capture.assert_called()

    with patch.object(container.processing_service, "reject_capture"):
        # emulate action
        response = client.get("/processing/cmd/reject")
        assert response.status_code == 200

        container.processing_service.reject_capture.assert_called()

    with patch.object(container.processing_service, "abort_process"):
        # emulate action
        response = client.get("/processing/cmd/abort")
        assert response.status_code == 200

        container.processing_service.abort_process.assert_called()
