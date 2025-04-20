import os
import tempfile
import uuid

from ..utils import extract_exact_position, save_figure_to_png, upload_image_to_drive


class GraphComponent:
    def __init__(self, slides_service, drive_service, presentation_id):
        self.slides_service = slides_service
        self.drive_service = drive_service
        self.presentation_id = presentation_id

    def insert(self, text_id: str, fig):
        presentation = (
            self.slides_service.presentations()
            .get(presentationId=self.presentation_id)
            .execute()
        )

        found = False
        object_id = f"image_{text_id.lower()}"
        slide_id = None
        position = None

        for slide in presentation["slides"]:
            for element in slide.get("pageElements", []):
                if "{{ " + text_id + " }}" in element.get("description", ""):
                    target_id = element["objectId"]
                    slide_id = slide["objectId"]
                    position = extract_exact_position(element)
                    found = True
                    break
            if found:
                break

        if not found:
            raise ValueError(f"No element found with alt text '{{{{ {text_id} }}}}'")

        # Save and upload figure
        tmpfile = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")
        save_figure_to_png(fig, tmpfile)
        image_url = upload_image_to_drive(self.drive_service, tmpfile)
        os.remove(tmpfile)

        requests = [
            # Remove the original placeholder
            {"deleteObject": {"objectId": target_id}},
            # Insert image with forced size/position
            {
                "createImage": {
                    "objectId": object_id,
                    "url": image_url,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": position["size"],
                        "transform": position["transform"],
                    },
                }
            },
            # Add alt text for accessibility/template match
            {
                "updatePageElementAltText": {
                    "objectId": object_id,
                    "description": "{{ " + text_id + " }}",
                    "title": "",
                }
            },
        ]

        self.slides_service.presentations().batchUpdate(
            presentationId=self.presentation_id, body={"requests": requests}
        ).execute()

    def update(self, text_id: str, fig):
        presentation = (
            self.slides_service.presentations()
            .get(presentationId=self.presentation_id)
            .execute()
        )

        found = False
        object_id = None

        for slide in presentation["slides"]:
            for element in slide.get("pageElements", []):
                if "image" in element and "{{ " + text_id + " }}" in element.get(
                    "description", ""
                ):
                    object_id = element["objectId"]
                    found = True
                    break
            if found:
                break

        if not object_id:
            raise ValueError(f"No image found with alt text '{{{{ {text_id} }}}}'")

        # Enregistrer et uploader l'image
        tmpfile = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")
        save_figure_to_png(fig, tmpfile)
        image_url = upload_image_to_drive(self.drive_service, tmpfile)
        os.remove(tmpfile)

        requests = [{"replaceImage": {"imageObjectId": object_id, "url": image_url}}]

        self.slides_service.presentations().batchUpdate(
            presentationId=self.presentation_id, body={"requests": requests}
        ).execute()
