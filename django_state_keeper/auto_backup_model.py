import os
import random
import string
import threading
from datetime import datetime
from threading import Thread
from time import sleep

import telegram
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django_state_keeper.packaging_backup_model import BackupPackaging


class AutoBackupService(models.Model):
    THREADS_BY_ID = {}
    SHOULD_CONTINUE_BY_THREAD_NAME = {}
    name = models.CharField(max_length=100, blank=False, null=False)
    packaging = models.ForeignKey(BackupPackaging, blank=False, null=False, on_delete=models.CASCADE)
    period_minutes = models.IntegerField(default=24 * 60 * 60, blank=False, null=False)
    bot_token = models.CharField(max_length=100, blank=False, null=False)
    chat_id = models.CharField(max_length=50, blank=False, null=False)


@receiver(post_save, sender=AutoBackupService)
def create_backup_thread(sender, instance: AutoBackupService, **kwargs):
    stop_last_thread_of_backup_service(instance)
    new_thread_name = f'backup-sender-{instance.id}' + generate_random_string(10)
    AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[new_thread_name] = True
    new_thread = Thread(name=new_thread_name, target=backup_sender_thread, args=(instance,))
    AutoBackupService.THREADS_BY_ID[instance.id] = new_thread
    new_thread.start()


@receiver(pre_delete, sender=AutoBackupService)
def delete_backup_thread(sender, instance, **kwargs):
    stop_last_thread_of_backup_service(instance)


def stop_last_thread_of_backup_service(instance: AutoBackupService):
    if AutoBackupService.THREADS_BY_ID.__contains__(instance.id):
        stopping_thread: Thread = AutoBackupService.THREADS_BY_ID[instance.id]
        AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[stopping_thread.name] = False


def backup_sender_thread(instance: AutoBackupService):
    while AutoBackupService.SHOULD_CONTINUE_BY_THREAD_NAME[threading.current_thread().name]:
        send_backup_in_telegram(instance)
        sleep(60 * instance.period_minutes)


def send_backup_in_telegram(instance: AutoBackupService):
    bot = telegram.Bot(token=instance.bot_token)
    package_path = instance.packaging.create_a_backup_package()
    caption = f'{instance.name}\n{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}'
    with open(package_path, 'rb') as file:
        bot.send_document(chat_id=instance.chat_id, document=file, caption=caption)
    os.remove(path=package_path)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
