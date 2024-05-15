from typing import Any

import pytest


def filter_response_headers(response: dict[str, Any]) -> dict[str, Any]:
    # Modify or exclude headers as needed
    # Exclude a header from the response
    response["headers"].pop("openai-organization", None)
    return response


@pytest.fixture(scope="function")
def vcr_config() -> dict[str, Any]:
    return {
        # Be sure to match the case of the header exactly
        "filter_headers": ["authorization", "api-key"],
        "before_record_response": filter_response_headers,
    }
