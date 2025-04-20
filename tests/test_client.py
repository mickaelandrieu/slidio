import pytest
from unittest.mock import patch, Mock
from slidio.client import SlidioClient

def test_client_initialization(mock_credentials, presentation_id):
    """Test the initialization of SlidioClient."""
    client = SlidioClient(mock_credentials, presentation_id)
    
    assert client.credentials == mock_credentials
    assert client.presentation_id == presentation_id
    assert hasattr(client, 'text')
    assert hasattr(client, 'graph')
    assert hasattr(client, 'table')

def test_client_from_template(mock_credentials):
    """Test creating a client from a template."""
    template_id = "template_id"
    new_title = "New Presentation"
    viewers_emails = ["viewer@example.com"]
    contributors_emails = ["contributor@example.com"]
    
    with patch('slidio.client.build') as mock_build:
        # Créer un mock pour le service Drive
        mock_drive_service = Mock()
        mock_build.return_value = mock_drive_service
        
        # Configurer le mock pour files().copy()
        mock_copy = Mock()
        mock_copy.execute.return_value = {"id": "new_presentation_id"}
        mock_drive_service.files().copy = Mock(return_value=mock_copy)
        
        # Configurer le mock pour permissions().create()
        mock_permission = Mock()
        mock_permission.execute.return_value = {"id": "permission_id"}
        mock_drive_service.permissions().create = Mock(return_value=mock_permission)
        
        # Créer le client
        client = SlidioClient.from_template(
            mock_credentials,
            template_id,
            new_title,
            viewers_emails,
            contributors_emails
        )
        
        # Vérifier que files().copy() a été appelé une seule fois
        mock_drive_service.files().copy.assert_called_once_with(
            fileId=template_id,
            body={"name": new_title}
        )
        
        # Vérifier que permissions().create() a été appelé deux fois
        assert mock_drive_service.permissions().create.call_count == 2
        
        # Vérifier que le client a été créé avec le bon ID de présentation
        assert client.presentation_id == "new_presentation_id"

def test_client_url_property(mock_credentials):
    """Test the URL property of SlidioClient."""
    presentation_id = "test_presentation_id"
    client = SlidioClient(mock_credentials, presentation_id)
    
    expected_url = f"https://docs.google.com/presentation/d/{presentation_id}"
    assert client.url == expected_url 