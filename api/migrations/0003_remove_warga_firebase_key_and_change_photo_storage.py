from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_warga_firebase_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warga',
            name='firebase_key',
        ),
        migrations.AlterField(
            model_name='warga',
            name='foto_rumah',
            field=models.FileField(blank=True, null=True, upload_to='warga/rumah/'),
        ),
    ]
