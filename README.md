# Django State Keeper

Django State Keeper is a Django app that allows you to create backups of your project's database, media files, and
selected directories. It provides the ability to restore your project's state from a backup and offers automatic backups
sent to a Telegram chat.

## Features

- Create backups as ZIP files containing selected project files and directories.
- Restore project state by uploading a backup ZIP file.
- Configure automatic backups sent to a Telegram chat.

## Installation

1. Install the Django State Keeper library using pip:

   ```shell
   pip install django-state-keeper
   ```

2. Add `django_state_keeper` to the INSTALLED_APPS list in your Django project's settings:

   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'django_state_keeper'
   ]
   ```

3. Include the Django State Keeper URL path in your project's urls.py file. Add the following line at the end of the
   urls.py:

   ```python
   urlpatterns += [path('your-customized-path/', include('django_state_keeper.urls'))]
   ```

   Replace `'your-customized-path/'` with the desired URL path where you want to access the Django State Keeper app.

4. Run migrations to create the necessary database tables:

   ```shell
   python manage.py migrate
   ```

5. Start the Django development server:

   ```shell
   python manage.py runserver
   ```

6. Access the Django State Keeper panel from Django admin site.

## How To Use

- You can create a "Backup Packaging" instance to customize your packaging method, and then you can create and download
  a backup by clicking on "Download" button.
- You can open the "Upload Backup" panel and upload a backup file to be injected immediately.
- You can create a "Auto Backup Sender Service" instance to receive backup files in telegram chat periodically.
## License

This project is licensed under the MIT License. See the LICENSE file for details.