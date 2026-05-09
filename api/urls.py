from django.urls import path

from .views import upload_profile_photo, upload_warga_media, warga_collection

urlpatterns = [
    path('warga/upload-media/', upload_warga_media),
    path('profile/upload-photo/', upload_profile_photo),
    path('warga/', warga_collection),
]
