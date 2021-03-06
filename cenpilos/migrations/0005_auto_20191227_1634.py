# Generated by Django 3.0.1 on 2019-12-27 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cenpilos', '0004_auto_20191226_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='blocked_users',
            field=models.ManyToManyField(related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=1000)),
                ('notifying_user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='notifying_users', to=settings.AUTH_USER_MODEL)),
                ('receiving_user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='receiving_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
