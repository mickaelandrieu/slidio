import pytest
from unittest.mock import patch, Mock, ANY
from slidio.utils import save_figure_to_png, upload_image_to_drive, extract_exact_position, extract_exact_transform
import os
import tempfile
import time

def test_save_figure_to_png(sample_figure):
    """Test saving a matplotlib figure to PNG."""
    # Utiliser le répertoire temporaire du système
    tmp_path = os.path.join(tempfile.gettempdir(), f"test_figure_{os.getpid()}.png")
    
    try:
        save_figure_to_png(sample_figure, tmp_path)
        assert os.path.exists(tmp_path)
        assert os.path.getsize(tmp_path) > 0
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except PermissionError:
                # On Windows, sometimes the file is still in use
                # We'll just log this and continue
                print(f"Warning: Could not remove temporary file {tmp_path}")

def test_upload_image_to_drive(mock_drive_service):
    """Test uploading an image to Google Drive."""
    # Mock the file creation response
    mock_drive_service.files().create().execute.return_value = {"id": "image_id"}
    
    # Mock the permissions creation
    mock_drive_service.permissions().create().execute.return_value = {}
    
    # Utiliser le répertoire temporaire du système
    tmp_path = os.path.join(tempfile.gettempdir(), f"test_image_{os.getpid()}.png")
    
    # Créer le fichier temporaire
    with open(tmp_path, 'wb') as tmp:
        tmp.write(b"test image data")
    
    # Appel de la fonction testée
    url = upload_image_to_drive(mock_drive_service, tmp_path)
    
    # Vérifications
    assert url == "https://drive.google.com/uc?id=image_id"
    
    # Verify the service was called correctly
    mock_drive_service.files().create.assert_called_with(
        body={'name': f"test_image_{os.getpid()}.png", 'mimeType': 'image/png'},
        media_body=ANY,
        fields='id'
    )
    mock_drive_service.permissions().create.assert_called_with(
        fileId='image_id',
        body={'type': 'anyone', 'role': 'reader'}
    )

def test_extract_exact_position():
    """Test extracting exact position from a page element."""
    element = {
        "transform": {
            "scaleX": 1.5,
            "scaleY": 2.0,
            "translateX": 100.0,
            "translateY": 200.0
        },
        "size": {
            "width": {
                "magnitude": 1.5,
                "unit": "PT"
            },
            "height": {
                "magnitude": 2.0,
                "unit": "PT"
            }
        }
    }
    
    position = extract_exact_position(element)
    
    assert position["size"]["width"]["magnitude"] == 1.5
    assert position["size"]["height"]["magnitude"] == 2.0
    assert position["transform"]["scaleX"] == 1.5
    assert position["transform"]["scaleY"] == 2.0
    assert position["transform"]["translateX"] == 100.0
    assert position["transform"]["translateY"] == 200.0

def test_extract_exact_transform():
    """Test extracting exact transform from a page element."""
    element = {
        "transform": {
            "scaleX": 1.5,
            "scaleY": 2.0,
            "translateX": 100.0,
            "translateY": 200.0
        }
    }
    
    transform = extract_exact_transform(element)
    
    assert transform["scaleX"] == 1
    assert transform["scaleY"] == 1
    assert transform["translateX"] == 100.0
    assert transform["translateY"] == 200.0
    assert transform["unit"] == "EMU" 