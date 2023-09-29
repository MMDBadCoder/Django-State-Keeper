from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_state_keeper.auto_backup_model import AutoBackupService
from django_state_keeper.loading_backup_model import BackupUpload
from django_state_keeper.packaging_backup_model import BackupPackaging


class AutoBackupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ['id']


admin.site.register(AutoBackupService, AutoBackupAdmin)


class BackupPackagingAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'download_button')
    ordering = ['id']

    def download_button(self, movie):
        url = reverse('admin-download-backup', args=[movie.id])
        button_html = f'<a class="button" href="{url}" target="_blank">Download</a>'
        return mark_safe(button_html)

    download_button.short_description = 'Download Backup'


admin.site.register(BackupPackaging, BackupPackagingAdmin)


class BackupUploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(BackupUpload, BackupUploadAdmin)
