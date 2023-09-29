import os
import random
import string
import sys
import threading
from datetime import datetime
from threading import Thread
from time import sleep

import telegram
from asgiref.sync import async_to_sync
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django_state_keeper.logging_utils import LoggerFactory
from django_state_keeper.packaging_backup_model import BackupPackaging


class AutoBackupService(models.Model):
    THREADS_BY_ID = {}
    SHOULD_CONTINUE_BY_THREAD_NAME = {}
    name = models.CharField(max_length=100, blank=False, null=False)
    packaging = models.ForeignKey(BackupPackaging, blank=False, null=False, on_delete=models.CASCADE)
    period_minutes = models.IntegerField(default=24 * 60 * 60, blank=False, null=False)
    bot_token = models.CharField(max_length=100, blank=False, null=False)
    chat_id = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Auto Backup Sender Service'
        verbose_name_plural = 'Auto Backup Sender Services'


@receiver(post_save, sender=AutoBackupService)
def create_backup_thread(sender, instance: AutoBackupService, **kwargs):
    stop_last_thread_of_backup_service(instance)
    create_new_thread_of_backup_service(instance)


@receiver(pre_delete, sender=AutoBackupService)
def delete_backup_thread(sender, instance, **kwargs):
    stop_last_thread_of_backup_service(instance)


def create_new_thread_of_backup_service(instance: AutoBackupService):
    new_thread_name = f'backup-sender-{instance.id}' + generate_random_string(10)
    AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[new_thread_name] = True
    new_thread = Thread(name=new_thread_name, target=backup_sender_thread, args=(instance,))
    AutoBackupService.THREADS_BY_ID[instance.id] = new_thread
    new_thread.start()
    LoggerFactory.get_instance().info(f'Thread of {instance.name} backup service was created.')


def stop_last_thread_of_backup_service(instance: AutoBackupService):
    if AutoBackupService.THREADS_BY_ID.__contains__(instance.id):
        stopping_thread: Thread = AutoBackupService.THREADS_BY_ID[instance.id]
        AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[stopping_thread.name] = False
        LoggerFactory.get_instance().info(f'Thread of {instance.name} backup service will no longer continue.')


def backup_sender_thread(instance: AutoBackupService):
    while AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[threading.current_thread().name]:
        try:
            send_backup_in_telegram(instance)
        except Exception as e:
            LoggerFactory.get_instance().error(e)
        sleep(60 * instance.period_minutes)
    LoggerFactory.get_instance().info(f'Thread of {instance.name} backup service ended.')


def send_backup_in_telegram(instance: AutoBackupService):
    bot = telegram.Bot(token=instance.bot_token)
    package_path = instance.packaging.create_a_backup_package()
    caption = f'{instance.name}\n{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}'
    with open(package_path, 'rb') as file:
        async def async_def():
            await bot.send_document(chat_id=instance.chat_id, document=file, caption=caption)

        async_to_sync(async_def)()
    os.remove(path=package_path)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
    for auto_backup in AutoBackupService.objects.all():
        create_new_thread_of_backup_service(auto_backup)
