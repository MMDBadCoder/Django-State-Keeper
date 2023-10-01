import os
import shutil
import sys
import tempfile
import threading
from datetime import datetime, timedelta
from time import sleep

from django.conf import settings
from django.core.exceptions import BadRequest
from django.db import models

from django_state_keeper.logging_utils import LoggerFactory


class BackupPackaging(models.Model):
    TIME_OF_ZIP_CREATION = {}
    name = models.CharField(max_length=100, blank=False, null=False)
    paths_to_gather = models.TextField(max_length=1000, blank=False, null=False, default='db.sqlite3')

    def __str__(self):
        return self.name

    def create_a_backup_package(self):
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy pase mentioned files and directories to a temporary directory
            for relative_source_path in self.paths_to_gather.split('\n'):
                relative_source_path = relative_source_path.strip()
                if not relative_source_path:
                    continue
                absolute_source_path = os.path.join(settings.BASE_DIR, relative_source_path)
                if os.path.isfile(absolute_source_path):
                    absolute_target_path = os.path.join(temp_dir, relative_source_path)
                    os.makedirs(os.path.dirname(absolute_target_path), exist_ok=True)
                    shutil.copy(absolute_source_path, absolute_target_path)
                elif os.path.isdir(absolute_source_path):
                    absolute_target_directory = os.path.join(temp_dir, relative_source_path)
                    shutil.copytree(absolute_source_path, absolute_target_directory)
                else:
                    LoggerFactory.get_instance().error("Invalid source path:", absolute_source_path)

            # Create a zip file containing all the files in the temporary directory
            zip_file_name = f'{self.name.replace(" ", "_")}-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
            creating_zip_path = os.path.join(tempfile.tempdir, zip_file_name)
            creating_zip_path = shutil.make_archive(creating_zip_path, 'zip', temp_dir)
            BackupPackaging.TIME_OF_ZIP_CREATION[creating_zip_path] = datetime.now()
            LoggerFactory.get_instance().info(f'{creating_zip_path} was created.')
            return creating_zip_path
        except Exception as e:
            raise BadRequest(e)


def created_zips_cleaner():
    hour_difference = timedelta(hours=1)
    while True:
        for created_zip_path, creation_time in BackupPackaging.TIME_OF_ZIP_CREATION.items():
            if datetime.now() - creation_time > hour_difference:
                try:
                    os.remove(created_zip_path)
                    del BackupPackaging.TIME_OF_ZIP_CREATION[created_zip_path]
                    LoggerFactory.get_instance().info(f'{created_zip_path} was deleted.')
                except Exception as e:
                    LoggerFactory.get_instance().error(e)
        sleep(hour_difference.seconds)


if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
    threading.Thread(target=created_zips_cleaner).start()
