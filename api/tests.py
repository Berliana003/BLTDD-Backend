import json
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import Warga


TEST_MEDIA_ROOT = Path(__file__).resolve().parent.parent / 'test_media'


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class WargaUploadTests(TestCase):
    def test_upload_profile_photo_saves_physical_file(self):
        profile_photo = SimpleUploadedFile(
            'profile.jpg',
            b'fake-profile-content',
            content_type='image/jpeg',
        )

        response = self.client.post(
            '/api/profile/upload-photo/',
            data={
                'profile_photo': profile_photo,
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = json.loads(response.content)
        self.assertIn('/media/profile/', payload['profile_photo'])

    def test_upload_media_saves_physical_files(self):
        rumah = SimpleUploadedFile(
            'rumah.jpg',
            b'fake-rumah-content',
            content_type='image/jpeg',
        )
        aset = SimpleUploadedFile(
            'aset.jpg',
            b'fake-aset-content',
            content_type='image/jpeg',
        )

        response = self.client.post(
            '/api/warga/upload-media/',
            data={
                'kepemilikan_aset': 'kendaraan',
                'foto_rumah': rumah,
                'foto_aset': aset,
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = json.loads(response.content)

        self.assertIn('/media/warga/rumah/', payload['foto_rumah'])
        self.assertEqual(len(payload['foto_aset']), 1)
        self.assertIn('/media/warga/aset/', payload['foto_aset'][0])

    def test_post_warga_saves_physical_files(self):
        rumah = SimpleUploadedFile(
            'rumah.jpg',
            b'fake-rumah-content',
            content_type='image/jpeg',
        )
        aset = SimpleUploadedFile(
            'aset.jpg',
            b'fake-aset-content',
            content_type='image/jpeg',
        )

        response = self.client.post(
            '/api/warga/',
            data={
                'nik': '1234567890123456',
                'nama': 'Budi',
                'alamat': 'Jl. Mawar',
                'jumlah_anggota': '4',
                'jumlah_tanggungan': '2',
                'status_kk': 'sendiri',
                'status_tinggal': 'tetap',
                'sumber_air': 'pam',
                'pendapatan': 'miskin',
                'pekerjaan': 'Petani',
                'status_pekerjaan': 'tetap',
                'kepemilikan_usaha': 'tidak',
                'kepemilikan_aset': 'kendaraan',
                'riwayat_bantuan': 'belum_pernah',
                'tanggal': '18/04/2026',
                'status_approval': 'Pending',
                'foto_rumah': rumah,
                'foto_aset': aset,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Warga.objects.count(), 1)

        warga = Warga.objects.get()
        payload = json.loads(response.content)

        self.assertTrue(warga.foto_rumah.name.startswith('warga/rumah/'))
        self.assertEqual(len(warga.foto_aset), 1)
        self.assertTrue(warga.foto_aset[0].startswith('warga/aset/'))
        self.assertIn('/media/warga/rumah/', payload['foto_rumah'])
        self.assertEqual(len(payload['foto_aset']), 1)
        self.assertIn('/media/warga/aset/', payload['foto_aset'][0])
