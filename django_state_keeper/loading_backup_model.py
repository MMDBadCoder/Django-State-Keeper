import os
import zipfile

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BackupUpload(models.Model):
    zip_file = models.FileField(upload_to='loaded_backup/', blank=True)

    class Meta:
        verbose_name = 'Upload Backup'
        verbose_name_plural = 'Upload Backup'

@receiver(post_save, sender=BackupUpload)
def create_backup_thread(sender, instance: BackupUpload, **kwargs):
    with zipfile.ZipFile(instance.zip_file.path, 'r') as zip_ref:
        zip_ref.extractall(settings.BASE_DIR)
    instance.delete()
    os.remove(instance.zip_file.path)
