# Generated by Django 4.2.5 on 2023-09-29 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_state_keeper', '0002_delete_backupupload_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_file', models.FileField(blank=True, upload_to='loaded_backup/')),
            ],
        ),
    ]
