from googleapiclient.discovery import build

from .components import GraphComponent, TableComponent, TextComponent


class SlidioClient:
    def __init__(self, credentials, presentation_id: str):
        self.credentials = credentials
        self.presentation_id = presentation_id

        self.slides_service = build("slides", "v1", credentials=credentials)
        self.drive_service = build("drive", "v3", credentials=credentials)

        self.text = TextComponent(self.slides_service, self.presentation_id)
        self.graph = GraphComponent(
            self.slides_service, self.drive_service, self.presentation_id
        )
        self.table = TableComponent(self.slides_service, self.presentation_id)

    @classmethod
    def from_template(
        cls,
        credentials,
        template_id: str,
        new_title: str,
        viewers_emails: list[str] | None = None,
        contributors_emails: list[str] | None = None,
    ):
        drive_service = build("drive", "v3", credentials=credentials)

        # 1. Copier le template
        copied = (
            drive_service.files()
            .copy(fileId=template_id, body={"name": new_title})
            .execute()
        )
        presentation_id = copied["id"]

        # 2. Partager avec les viewers (lecture/commentaire)
        if viewers_emails:
            for email in viewers_emails:
                drive_service.permissions().create(
                    fileId=presentation_id,
                    body={"type": "user", "role": "commenter", "emailAddress": email},
                    fields="id",
                ).execute()

        # 3. Partager avec les contributors (édition)
        if contributors_emails:
            for email in contributors_emails:
                drive_service.permissions().create(
                    fileId=presentation_id,
                    body={"type": "user", "role": "writer", "emailAddress": email},
                    fields="id",
                ).execute()

        return cls(credentials, presentation_id)

    @property
    def url(self):
        return f"https://docs.google.com/presentation/d/{self.presentation_id}"
