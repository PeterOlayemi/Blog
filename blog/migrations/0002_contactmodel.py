# Generated by Django 4.1.4 on 2023-03-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.CharField(max_length=249)),
                ('whatsapp', models.CharField(max_length=249)),
                ('instagram', models.CharField(max_length=249)),
                ('twitter', models.CharField(max_length=249)),
                ('github', models.CharField(max_length=249)),
            ],
        ),
    ]
