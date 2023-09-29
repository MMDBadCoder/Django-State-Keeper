from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse

from django_state_keeper.packaging_backup_model import BackupPackaging


@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_file_view(request, packaging_id):
    packaging_instance = BackupPackaging.objects.get(id=packaging_id)
    created_zip_path = packaging_instance.create_a_backup_package()
    response = FileResponse(open(created_zip_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(created_zip_path)
    return response
