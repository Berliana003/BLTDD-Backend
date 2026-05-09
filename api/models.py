from django.db import models

class Warga(models.Model):
    nik = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    jumlah_anggota = models.IntegerField()
    jumlah_tanggungan = models.IntegerField()
    status_kk = models.CharField(max_length=50, blank=True, default='')
    status_tinggal = models.CharField(max_length=50, blank=True, default='')
    sumber_air = models.CharField(max_length=50, blank=True, default='')
    pendapatan = models.CharField(max_length=50)
    pekerjaan = models.CharField(max_length=100)
    status_pekerjaan = models.CharField(max_length=50, blank=True, default='')
    kepemilikan_usaha = models.CharField(max_length=20, blank=True, default='')
    kepemilikan_aset = models.CharField(max_length=50, blank=True, default='')
    riwayat_bantuan = models.CharField(max_length=50, blank=True, default='')
    foto_rumah = models.FileField(upload_to='warga/rumah/', null=True, blank=True)
    foto_aset = models.JSONField(blank=True, default=list)
    tanggal = models.CharField(max_length=30, blank=True, default='')
    status = models.CharField(max_length=20, blank=True, null=True, default=None)
    nilai_akhir = models.FloatField(blank=True, null=True, default=None)
    status_approval = models.CharField(max_length=20, blank=True, default='Pending')
    def __str__(self):
        return self.nama
