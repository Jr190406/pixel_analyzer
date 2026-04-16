# Generated migration to recreate RequestMessage table if missing

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0013_recreate_requeststatuschange'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_internal_note', models.BooleanField(default=False, help_text='Internal notes only visible to super admin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_by_user', models.BooleanField(default=False, help_text='Has the requesting user read this message')),
                ('read_by_admin', models.BooleanField(default=False, help_text='Has the super admin read this message')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='analyzer.businessownerrequest')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Request Message',
                'verbose_name_plural': 'Request Messages',
                'ordering': ['created_at'],
            },
        ),
    ]