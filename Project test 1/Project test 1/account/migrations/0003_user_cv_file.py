# Generated by Django 5.1.4 on 2024-12-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='CV_file',
            field=models.FileField(blank=True, null=True, upload_to='cvs/'),
        ),
    ]
