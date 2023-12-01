# Generated by Django 4.2.6 on 2023-11-28 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rodManager', '0013_merge_0007_garden_0012_alter_garden_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaseholderID', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='garden',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField()),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='rodManager.document')),
            ],
        ),
    ]
