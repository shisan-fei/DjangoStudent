# Generated by Django 2.2.6 on 2022-03-28 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoStudent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.OneToOneField(db_column='username', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='DjangoStudent.Students', verbose_name='用户名')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 't_user',
            },
        ),
    ]
