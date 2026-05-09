import os
from uuid import uuid4

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Warga


def home(request):
    return JsonResponse({
        "message": "Backend BLT berhasil berjalan"
    })


def build_media_url(request, path):
    if not path:
        return ''

    url = default_storage.url(path)
    return request.build_absolute_uri(url) if request is not None else url


def save_uploaded_file(file_obj, folder):
    extension = os.path.splitext(file_obj.name)[1]
    filename = f"warga/{folder}/{uuid4().hex}{extension}"
    saved_path = default_storage.save(filename, file_obj)
    return saved_path


def save_profile_file(file_obj):
    extension = os.path.splitext(file_obj.name)[1]
    filename = f"profile/{uuid4().hex}{extension}"
    saved_path = default_storage.save(filename, file_obj)
    return saved_path


def serialize_warga(warga, request=None):
    return {
        "id": warga.id,
        "nik": warga.nik,
        "nama": warga.nama,
        "alamat": warga.alamat,
        "jumlah_anggota": warga.jumlah_anggota,
        "jumlah_tanggungan": warga.jumlah_tanggungan,
        "status_kk": warga.status_kk,
        "status_tinggal": warga.status_tinggal,
        "sumber_air": warga.sumber_air,
        "pendapatan": warga.pendapatan,
        "pekerjaan": warga.pekerjaan,
        "status_pekerjaan": warga.status_pekerjaan,
        "kepemilikan_usaha": warga.kepemilikan_usaha,
        "kepemilikan_aset": warga.kepemilikan_aset,
        "riwayat_bantuan": warga.riwayat_bantuan,
        "foto_rumah": (
            request.build_absolute_uri(warga.foto_rumah.url)
            if request is not None and warga.foto_rumah
            else (warga.foto_rumah.url if warga.foto_rumah else '')
        ),
        "foto_aset": [build_media_url(request, path) for path in warga.foto_aset],
        "tanggal": warga.tanggal,
        "status": warga.status,
        "nilai_akhir": warga.nilai_akhir,
        "status_approval": warga.status_approval,
    }


@csrf_exempt
def upload_warga_media(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    foto_rumah = request.FILES.get('foto_rumah')
    foto_aset_files = request.FILES.getlist('foto_aset')
    kepemilikan_aset = request.POST.get('kepemilikan_aset', 'tidak')

    if foto_rumah is None:
        return JsonResponse({"error": "Foto rumah wajib diupload"}, status=400)

    if kepemilikan_aset != 'tidak' and not foto_aset_files:
        return JsonResponse({"error": "Foto aset wajib diupload"}, status=400)

    saved_rumah_path = save_uploaded_file(foto_rumah, 'rumah')
    saved_aset_paths = [
        save_uploaded_file(foto, 'aset') for foto in foto_aset_files
    ]

    return JsonResponse(
        {
            "foto_rumah": build_media_url(request, saved_rumah_path),
            "foto_aset": [build_media_url(request, path) for path in saved_aset_paths],
        },
        status=201,
    )


@csrf_exempt
def upload_profile_photo(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    profile_photo = request.FILES.get('profile_photo')

    if profile_photo is None:
        return JsonResponse({"error": "Foto profil wajib diupload"}, status=400)

    saved_profile_path = save_profile_file(profile_photo)

    return JsonResponse(
        {
            "profile_photo": build_media_url(request, saved_profile_path),
        },
        status=201,
    )


@csrf_exempt
def warga_collection(request):
    if request.method == 'GET':
        data = [serialize_warga(warga, request) for warga in Warga.objects.all().order_by('-id')]
        return JsonResponse(data, safe=False)

    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    payload = request.POST
    required_fields = [
        'nik',
        'nama',
        'alamat',
        'jumlah_anggota',
        'jumlah_tanggungan',
        'pendapatan',
        'pekerjaan',
    ]
    missing_fields = [field for field in required_fields if payload.get(field) in (None, '')]
    if missing_fields:
        return JsonResponse(
            {"error": f"Field wajib belum lengkap: {', '.join(missing_fields)}"},
            status=400,
        )

    foto_rumah = request.FILES.get('foto_rumah')
    foto_aset_files = request.FILES.getlist('foto_aset')

    if foto_rumah is None:
        return JsonResponse({"error": "Foto rumah wajib diupload"}, status=400)

    if payload.get('kepemilikan_aset') != 'tidak' and not foto_aset_files:
        return JsonResponse({"error": "Foto aset wajib diupload"}, status=400)

    saved_rumah_path = save_uploaded_file(foto_rumah, 'rumah')
    saved_aset_paths = [save_uploaded_file(foto, 'aset') for foto in foto_aset_files]

    warga = Warga.objects.create(
        nik=payload['nik'],
        nama=payload['nama'],
        alamat=payload['alamat'],
        jumlah_anggota=int(payload['jumlah_anggota']),
        jumlah_tanggungan=int(payload['jumlah_tanggungan']),
        status_kk=payload.get('status_kk', ''),
        status_tinggal=payload.get('status_tinggal', ''),
        sumber_air=payload.get('sumber_air', ''),
        pendapatan=payload['pendapatan'],
        pekerjaan=payload['pekerjaan'],
        status_pekerjaan=payload.get('status_pekerjaan', ''),
        kepemilikan_usaha=payload.get('kepemilikan_usaha', ''),
        kepemilikan_aset=payload.get('kepemilikan_aset', ''),
        riwayat_bantuan=payload.get('riwayat_bantuan', ''),
        foto_rumah=saved_rumah_path,
        foto_aset=saved_aset_paths,
        tanggal=payload.get('tanggal', ''),
        status=payload.get('status') or None,
        nilai_akhir=payload.get('nilai_akhir') or None,
        status_approval=payload.get('status_approval', 'Pending'),
    )

    return JsonResponse(serialize_warga(warga, request), status=201)
