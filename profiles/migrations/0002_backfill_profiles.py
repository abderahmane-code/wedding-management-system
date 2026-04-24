"""Create a Profile row for any User that doesn't already have one.

Handy when this app is added to an existing deployment that already has users.
"""
from django.db import migrations


def backfill_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("profiles", "Profile")
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


def noop(apps, schema_editor):
    # Nothing to reverse — we don't delete user-owned profile rows on rollback.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(backfill_profiles, noop),
    ]
