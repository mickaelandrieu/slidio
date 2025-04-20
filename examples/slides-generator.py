import matplotlib.pyplot as plt
from google.oauth2 import service_account

from slidio import SlidioClient

creds = service_account.Credentials.from_service_account_file(
    "examples/credentials.json",
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/presentations",
    ],
)

client = SlidioClient.from_template(
    credentials=creds,
    template_id="1V7Cc7vgvgLvqeqQjL11CtZkT-10a6yU-3HcFAP3PwNw",
    new_title="📊 Weekly Report",
    contributors_emails=["mickael.andrieu@solvolabs.com"],
)

# Update a text
client.text.update("TITLE", "Weekly Report")

# Update a picture
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [5, 4, 6])
ax.set_title("Sales over Time")

client.graph.update("IMG1", fig)

# update a table
table_data = [
    ["Product", "Units Sold", "Revenue", "Status"],
    ["Widget A", "120", "$1,200", "✅"],
    ["Widget B", "95", "$950", "✅"],
    ["Widget C", "142", "$1,420", "😅"],
    ["Widget D", "68", "$680", "😢"],
]

client.table.update("TABLE1", table_data)

print(f"✅ Done! View your slides: {client.url}")
