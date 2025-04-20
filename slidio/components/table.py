from ..utils import extract_exact_transform


class TableComponent:
    def __init__(self, slides_service, presentation_id):
        self.slides_service = slides_service
        self.presentation_id = presentation_id

    def insert(self, text_id: str, data: list[list[str]]):
        presentation = (
            self.slides_service.presentations()
            .get(presentationId=self.presentation_id)
            .execute()
        )

        found = False
        object_id = f"table_{text_id.lower()}"
        slide_id = None
        transform = None

        for slide in presentation["slides"]:
            for element in slide.get("pageElements", []):
                if "{{ " + text_id + " }}" in element.get("description", ""):
                    target_id = element["objectId"]
                    slide_id = slide["objectId"]
                    transform = extract_exact_transform(element)
                    found = True
                    break
            if found:
                break

        if not found:
            raise ValueError(f"No element found with alt text '{{{{ {text_id} }}}}'")

        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0

        requests = [
            {"deleteObject": {"objectId": target_id}},
            {
                "createTable": {
                    "objectId": object_id,
                    "rows": rows,
                    "columns": cols,
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "transform": transform,
                    },
                }
            },
        ]

        for r, row in enumerate(data):
            for c, text in enumerate(row):
                requests.append(
                    {
                        "insertText": {
                            "objectId": object_id,
                            "cellLocation": {"rowIndex": r, "columnIndex": c},
                            "text": str(text),
                        }
                    }
                )

                if r == 0:
                    requests.append(
                        {
                            "updateTextStyle": {
                                "objectId": object_id,
                                "cellLocation": {"rowIndex": r, "columnIndex": c},
                                "style": {"bold": True},
                                "fields": "bold",
                            }
                        }
                    )

        requests.append(
            {
                "updatePageElementAltText": {
                    "objectId": object_id,
                    "description": "{{ " + text_id + " }}",
                    "title": "",
                }
            }
        )

        self.slides_service.presentations().batchUpdate(
            presentationId=self.presentation_id, body={"requests": requests}
        ).execute()

    def update(self, text_id: str, data: list[list[str]]):
        presentation = (
            self.slides_service.presentations()
            .get(presentationId=self.presentation_id)
            .execute()
        )

        table_id = None
        found = False
        existing_rows = 0

        for slide in presentation["slides"]:
            for element in slide.get("pageElements", []):
                if "table" in element and "{{ " + text_id + " }}" in element.get(
                    "description", ""
                ):
                    table_id = element["objectId"]
                    existing_rows = element["table"]["rows"]
                    found = True
                    break
            if found:
                break

        if not table_id:
            raise ValueError(f"No table found with alt text '{{{{ {text_id} }}}}'")

        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0
        requests = []

        # Ajouter des lignes si nécessaire
        if rows > existing_rows:
            requests.append(
                {
                    "insertTableRows": {
                        "tableObjectId": table_id,
                        "cellLocation": {
                            "rowIndex": existing_rows - 1,
                            "columnIndex": 0,
                        },
                        "insertBelow": True,
                        "number": rows - existing_rows,
                    }
                }
            )

        # Mettre à jour les cellules
        for r in range(rows):
            for c in range(cols):
                requests.append(
                    {
                        "insertText": {
                            "objectId": table_id,
                            "cellLocation": {"rowIndex": r, "columnIndex": c},
                            "text": str(data[r][c]),
                            "insertionIndex": 0,
                        }
                    }
                )

        self.slides_service.presentations().batchUpdate(
            presentationId=self.presentation_id, body={"requests": requests}
        ).execute()
