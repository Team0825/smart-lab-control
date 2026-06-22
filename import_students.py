import os
import django
import pandas as pd

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "labcontrol.settings"
)

django.setup()

from monitoring.models import Student

df = pd.read_excel("students.xlsx")

print("Rows found:", len(df))

for _, row in df.iterrows():

    Student.objects.get_or_create(
        registration_number=str(row["registration_number"]),
        defaults={
            "name": str(row["name"]),
            "department": str(row["department"]),
            "semester": str(row["semester"]),
        }
    )

print("Import Completed")
print("Students:", Student.objects.count())