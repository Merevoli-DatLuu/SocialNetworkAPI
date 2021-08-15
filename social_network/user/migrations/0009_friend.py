# Generated by Django 3.2 on 2021-08-04 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('Accept', 'Accept')], default='New', max_length=10)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user_source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_user_source', to=settings.AUTH_USER_MODEL)),
                ('user_target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_user_target', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_source', 'user_target')},
            },
        ),
    ]