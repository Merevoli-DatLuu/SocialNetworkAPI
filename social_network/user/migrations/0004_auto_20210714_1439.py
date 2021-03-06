# Generated by Django 3.2.5 on 2021-07-14 07:39

from django.db import migrations, models
import user.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210714_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(validators=[user.validators.validate_age]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100, validators=[user.validators.validate_secure_email]),
        ),
    ]
