import os

from googleapiclient.http import MediaFileUpload


def upload_image_to_drive(drive_service, image_path):
    file_metadata = {"name": os.path.basename(image_path), "mimeType": "image/png"}
    media = MediaFileUpload(image_path, mimetype="image/png")
    uploaded = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    drive_service.permissions().create(
        fileId=uploaded["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return f"https://drive.google.com/uc?id={uploaded['id']}"


def save_figure_to_png(fig, filepath):
    fig.savefig(filepath, format="png", bbox_inches="tight")
    fig.clf()


def extract_exact_position(element):
    return {"size": element["size"], "transform": element["transform"]}


def extract_exact_transform(element):
    return {
        "scaleX": 1,
        "scaleY": 1,
        "translateX": element["transform"].get("translateX", 0),
        "translateY": element["transform"].get("translateY", 0),
        "unit": "EMU",
    }
