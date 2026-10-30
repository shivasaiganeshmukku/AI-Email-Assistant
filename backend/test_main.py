
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AI Email Assistant"
    }


def test_empty_email_body_is_rejected():
    response = client.post(
        "/api/summarize-email",
        json={
            "sender": "manager@company.com",
            "recipient": "you@company.com",
            "subject": "Project Report",
            "body": ""
        }
    )

    assert response.status_code == 422


def test_invalid_reply_tone_is_rejected():
    response = client.post(
        "/api/generate-reply",
        json={
            "email": {
                "sender": "manager@company.com",
                "recipient": "you@company.com",
                "subject": "Project Report",
                "body": "Please share the report by Friday."
            },
            "tone": "Funny"
        }
    )

    assert response.status_code == 422


def test_analyze_email_returns_structured_result():
    ai_response = (
        '{"summary": "A report is requested by Friday.", '
        '"category": "Work", '
        '"priority": "High", '
        '"action_required": true, '
        '"email_status": "Action Required", '
        '"deadline": "Friday", '
        '"recommended_action": "Prepare and send the report."}'
    )

    with patch(
        "main.generate_response",
        new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = ai_response

        response = client.post(
            "/api/analyze-email",
            json={
                "sender": "manager@company.com",
                "recipient": "you@company.com",
                "subject": "Project Report",
                "body": "Please share the report by Friday."
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "A report is requested by Friday.",
        "category": "Work",
        "priority": "High",
        "action_required": True,
        "email_status": "Action Required",
        "deadline": "Friday",
        "recommended_action": "Prepare and send the report."
    }

    mock_generate.assert_awaited_once()


def test_summarize_email_returns_summary():
    ai_response = (
        "The manager requests the project report by Friday."
    )

    with patch(
        "main.generate_response",
        new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = ai_response

        response = client.post(
            "/api/summarize-email",
            json={
                "sender": "manager@company.com",
                "recipient": "you@company.com",
                "subject": "Project Report",
                "body": (
                    "Please complete and share the project "
                    "report by Friday."
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["subject"] == "Project Report"
    assert data["summary"] == ai_response

    mock_generate.assert_awaited_once()


def test_classify_email_returns_valid_category():
    ai_response = '{"category": "Finance"}'

    with patch(
        "main.generate_response",
        new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = ai_response

        response = client.post(
            "/api/classify-email",
            json={
                "sender": "accounts@company.com",
                "recipient": "you@company.com",
                "subject": "Invoice Payment",
                "body": (
                    "Please review the invoice and process "
                    "the payment by Friday."
                )
            }
        )

    assert response.status_code == 200
    assert response.json() == {"category": "Finance"}

    mock_generate.assert_awaited_once()


def test_extract_action_returns_action_items():
    ai_response = (
        '{"action_items": ['
        '{"task": "Prepare the report", '
        '"deadline": "Friday", '
        '"assignee": "You"}, '
        '{"task": "Review the report", '
        '"deadline": null, '
        '"assignee": "John"}'
        ']}'
    )

    with patch(
        "main.generate_response",
        new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = ai_response

        response = client.post(
            "/api/extract-action",
            json={
                "sender": "manager@company.com",
                "recipient": "you@company.com",
                "subject": "Project Report",
                "body": (
                    "Please prepare the report by Friday. "
                    "John will review the report."
                )
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "action_items": [
            {
                "task": "Prepare the report",
                "deadline": "Friday",
                "assignee": "You"
            },
            {
                "task": "Review the report",
                "deadline": None,
                "assignee": "John"
            }
        ]
    }

    mock_generate.assert_awaited_once()


def test_generate_reply_returns_reply():
    ai_response = (
        "Dear Manager,\n\n"
        "Thank you for your request for the project report.\n\n"
        "Best regards"
    )

    with patch(
        "main.generate_response",
        new_callable=AsyncMock
    ) as mock_generate:
        mock_generate.return_value = ai_response

        response = client.post(
            "/api/generate-reply",
            json={
                "email": {
                    "sender": "manager@company.com",
                    "recipient": "you@company.com",
                    "subject": "Project Report",
                    "body": (
                        "Please share the project report by Friday."
                    )
                },
                "tone": "Professional"
            }
        )

    assert response.status_code == 200
    assert response.json() == {
        "subject": "Re: Project Report",
        "body": ai_response,
        "tone": "Professional"
    }

    mock_generate.assert_awaited_once()
