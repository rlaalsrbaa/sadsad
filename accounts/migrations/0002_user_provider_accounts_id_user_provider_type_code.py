
from django.db import migrations, models

from accounts.gen_master_data import gen_master


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='provider_accounts_id',
            field=models.PositiveIntegerField(default=0, verbose_name='프로바이더 회원번호'),
        ),
        migrations.AddField(
            model_name='user',
            name='provider_type_code',
            field=models.CharField(choices=[('local', '로컬'), ('kakao', '카카오')], default='local', max_length=20,
                                   verbose_name='프로바이더 타입코드'),
        ),
        migrations.RunPython(gen_master),
    ]