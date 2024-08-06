# Generated by Django 5.0.7 on 2024-08-05 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='image',
        ),
        migrations.CreateModel(
            name='NoticeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='notices')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='service.notice')),
            ],
        ),
    ]
