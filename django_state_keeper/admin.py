from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.urls.exceptions import NoReverseMatch
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
        try:
            url = reverse('admin-download-backup', args=[movie.id])
        except NoReverseMatch:
            raise Exception("You should include django-state-keeper.urls to your project urls!"
                            "\nAdd something like this in your urls.py file:"
                            "\n\"urlpatterns += [path('your-customized-path/', include('django_state_keeper.urls'))]\"")

        button_html = f'<a class="button" href="{url}" target="_blank">Download</a>'
        return mark_safe(button_html)

    download_button.short_description = 'Download Backup'


admin.site.register(BackupPackaging, BackupPackagingAdmin)


class BackupUploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(BackupUpload, BackupUploadAdmin)
