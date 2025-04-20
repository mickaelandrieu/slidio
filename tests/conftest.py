import pytest
from unittest.mock import Mock, patch
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import os

@pytest.fixture
def mock_credentials():
    """Mock Google credentials for testing."""
    return Mock(spec=service_account.Credentials)

@pytest.fixture
def mock_slides_service():
    """Mock Google Slides service."""
    return Mock()

@pytest.fixture
def mock_drive_service():
    """Mock Google Drive service."""
    return Mock()

@pytest.fixture
def presentation_id():
    """Sample presentation ID for testing."""
    return "test_presentation_id"

@pytest.fixture
def sample_figure():
    """Create a sample matplotlib figure for testing."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    return fig

@pytest.fixture
def sample_table_data():
    """Sample table data for testing."""
    return [
        ["Name", "Score"],
        ["John", "85"],
        ["Jane", "92"]
    ]

@pytest.fixture
def mock_presentation():
    """Mock presentation data structure."""
    return {
        "slides": [
            {
                "objectId": "slide1",
                "pageElements": [
                    {
                        "objectId": "text1",
                        "description": "{{ TITLE }}",
                        "shape": {
                            "text": {
                                "textElements": [
                                    {"textRun": {"content": "Old Title"}}
                                ]
                            }
                        }
                    },
                    {
                        "objectId": "graph1",
                        "description": "{{ GRAPH1 }}",
                        "transform": {
                            "scaleX": 1.0,
                            "scaleY": 1.0,
                            "translateX": 0.0,
                            "translateY": 0.0
                        },
                        "size": {
                            "width": {
                                "magnitude": 1.0,
                                "unit": "PT"
                            },
                            "height": {
                                "magnitude": 1.0,
                                "unit": "PT"
                            }
                        }
                    },
                    {
                        "objectId": "table1",
                        "description": "{{ TABLE1 }}",
                        "transform": {
                            "scaleX": 1.0,
                            "scaleY": 1.0,
                            "translateX": 0.0,
                            "translateY": 0.0
                        },
                        "table": {
                            "rows": 2,
                            "columns": 2,
                            "tableRows": [
                                {
                                    "tableCells": [
                                        {"text": {"textElements": [{"textRun": {"content": "Name"}}]}},
                                        {"text": {"textElements": [{"textRun": {"content": "Score"}}]}}
                                    ]
                                },
                                {
                                    "tableCells": [
                                        {"text": {"textElements": [{"textRun": {"content": "John"}}]}},
                                        {"text": {"textElements": [{"textRun": {"content": "85"}}]}}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    } 