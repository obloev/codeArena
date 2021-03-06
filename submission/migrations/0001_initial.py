# Generated by Django 3.2.3 on 2021-08-21 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(editable=False, max_length=5, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=50)),
                ('status_id', models.PositiveSmallIntegerField()),
                ('language', models.CharField(max_length=50)),
                ('lang_id', models.PositiveSmallIntegerField()),
                ('memory', models.PositiveIntegerField()),
                ('time', models.PositiveIntegerField()),
                ('code', models.TextField()),
                ('err', models.TextField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
