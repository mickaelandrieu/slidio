import pytest
from unittest.mock import patch, Mock
from slidio.components import TextComponent, GraphComponent, TableComponent
import os
import tempfile

def test_text_component_update(mock_slides_service, presentation_id, mock_presentation):
    """Test updating text in a presentation."""
    text_component = TextComponent(mock_slides_service, presentation_id)
    
    # Configurer le mock pour presentations().get()
    mock_get = Mock()
    mock_get.execute.return_value = mock_presentation
    mock_slides_service.presentations().get = Mock(return_value=mock_get)
    
    # Configurer le mock pour presentations().batchUpdate()
    mock_batch_update = Mock()
    mock_batch_update.execute.return_value = {}
    mock_slides_service.presentations().batchUpdate = Mock(return_value=mock_batch_update)
    
    # Test updating text
    text_component.update("TITLE", "New Title")
    
    # Vérifier que batchUpdate a été appelé une seule fois
    mock_slides_service.presentations().batchUpdate.assert_called_once()
    
    # Test error case
    with pytest.raises(ValueError):
        text_component.update("NONEXISTENT", "Some text")

def test_graph_component_insert(mock_slides_service, mock_drive_service, presentation_id, mock_presentation, sample_figure):
    """Test inserting a graph in a presentation."""
    graph_component = GraphComponent(mock_slides_service, mock_drive_service, presentation_id)
    
    # Configurer le mock pour presentations().get()
    mock_get = Mock()
    mock_get.execute.return_value = mock_presentation
    mock_slides_service.presentations().get = Mock(return_value=mock_get)
    
    # Configurer le mock pour presentations().batchUpdate()
    mock_batch_update = Mock()
    mock_batch_update.execute.return_value = {}
    mock_slides_service.presentations().batchUpdate = Mock(return_value=mock_batch_update)
    
    # Mock the image upload
    mock_drive_service.files().create().execute.return_value = {"id": "image_id"}
    mock_drive_service.files().get().execute.return_value = {"webContentLink": "https://example.com/image.png"}
    
    # Créer un fichier temporaire
    tmp_path = os.path.join(tempfile.gettempdir(), f"test_graph_{os.getpid()}.png")
    
    try:
        # Mock save_figure_to_png pour créer le fichier
        with patch('slidio.components.graph.save_figure_to_png') as mock_save:
            mock_save.side_effect = lambda fig, path: sample_figure.savefig(path)
            
            # Mock os.remove pour éviter les erreurs de suppression
            with patch('os.remove') as mock_remove:
                # Test inserting graph
                graph_component.insert("GRAPH1", sample_figure)
                
                # Verify the service was called correctly
                mock_slides_service.presentations().batchUpdate.assert_called_once()
                mock_save.assert_called_once()
                mock_remove.assert_called_once()
                
                # Test error case
                with pytest.raises(ValueError):
                    graph_component.insert("NONEXISTENT", sample_figure)
    finally:
        # Nettoyer le fichier temporaire s'il existe
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except PermissionError:
                print(f"Warning: Could not remove temporary file {tmp_path}")

def test_table_component_insert(mock_slides_service, presentation_id, mock_presentation, sample_table_data):
    """Test inserting a table in a presentation."""
    table_component = TableComponent(mock_slides_service, presentation_id)
    
    # Configurer le mock pour presentations().get()
    mock_get = Mock()
    mock_get.execute.return_value = mock_presentation
    mock_slides_service.presentations().get = Mock(return_value=mock_get)
    
    # Configurer le mock pour presentations().batchUpdate()
    mock_batch_update = Mock()
    mock_batch_update.execute.return_value = {}
    mock_slides_service.presentations().batchUpdate = Mock(return_value=mock_batch_update)
    
    # Test inserting table
    table_component.insert("TABLE1", sample_table_data)
    
    # Verify the service was called correctly
    mock_slides_service.presentations().batchUpdate.assert_called_once()
    
    # Test error case
    with pytest.raises(ValueError):
        table_component.insert("NONEXISTENT", sample_table_data)

def test_table_component_update(mock_slides_service, presentation_id, mock_presentation, sample_table_data):
    """Test updating a table in a presentation."""
    table_component = TableComponent(mock_slides_service, presentation_id)
    
    # Configurer le mock pour presentations().get()
    mock_get = Mock()
    mock_get.execute.return_value = mock_presentation
    mock_slides_service.presentations().get = Mock(return_value=mock_get)
    
    # Configurer le mock pour presentations().batchUpdate()
    mock_batch_update = Mock()
    mock_batch_update.execute.return_value = {}
    mock_slides_service.presentations().batchUpdate = Mock(return_value=mock_batch_update)
    
    # Test updating table
    table_component.update("TABLE1", sample_table_data)
    
    # Verify the service was called correctly
    mock_slides_service.presentations().batchUpdate.assert_called_once()
    
    # Test error case
    with pytest.raises(ValueError):
        table_component.update("NONEXISTENT", sample_table_data) 