# Generated migration for adding edited_by field to MessageHistory

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("messaging", "0001_initial"),  # Replace with your actual previous migration
    ]

    operations = [
        migrations.AddField(
            model_name="messagehistory",
            name="edited_by",
            field=models.ForeignKey(
                help_text="User who made this edit",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="message_edits",
                to=settings.AUTH_USER_MODEL,
                default=1,  # Temporary default for existing records
            ),
            preserve_default=False,
        ),
    ]
