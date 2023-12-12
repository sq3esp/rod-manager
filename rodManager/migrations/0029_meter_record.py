# Generated by Django 4.2.6 on 2023-12-12 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodManager', '0028_userdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('serial', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=200)),
                ('adress', models.CharField(max_length=200)),
                ('garden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rodManager.garden')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('value', models.FloatField()),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rodManager.meter')),
            ],
        ),
    ]
