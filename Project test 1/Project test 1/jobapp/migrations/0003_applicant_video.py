# Generated by Django 5.1.4 on 2024-12-22 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0002_contact_alter_applicant_id_alter_bookmarkjob_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
