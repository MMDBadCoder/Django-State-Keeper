# Generated by Django 4.2.5 on 2023-09-29 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupPackaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('paths_to_gather', models.TextField(default='db.sqlite', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='BackupUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='loaded_backup/')),
            ],
        ),
        migrations.CreateModel(
            name='AutoBackupService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('period_minutes', models.IntegerField(default=86400)),
                ('bot_token', models.CharField(max_length=100)),
                ('chat_id', models.CharField(max_length=50)),
                ('packaging', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_state_keeper.backuppackaging')),
            ],
        ),
    ]
