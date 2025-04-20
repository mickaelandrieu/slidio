class TextComponent:
    def __init__(self, slides_service, presentation_id):
        self.slides_service = slides_service
        self.presentation_id = presentation_id

    def update(self, text_id: str, text_value: str):
        presentation = (
            self.slides_service.presentations()
            .get(presentationId=self.presentation_id)
            .execute()
        )

        for slide in presentation["slides"]:
            for element in slide.get("pageElements", []):
                if "{{ " + text_id + " }}" in element.get("description", ""):
                    object_id = element["objectId"]
                    requests = [
                        {
                            "deleteText": {
                                "objectId": object_id,
                                "textRange": {"type": "ALL"},
                            }
                        },
                        {
                            "insertText": {
                                "objectId": object_id,
                                "insertionIndex": 0,
                                "text": text_value,
                            }
                        },
                    ]
                    self.slides_service.presentations().batchUpdate(
                        presentationId=self.presentation_id, body={"requests": requests}
                    ).execute()
                    return

        raise ValueError(f"No text box found with alt text '{{{{ {text_id} }}}}'")
