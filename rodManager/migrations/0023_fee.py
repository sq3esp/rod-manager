# Generated by Django 4.2.6 on 2023-12-10 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rodManager", "0022_billingperiod"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fee",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("fee_type", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("calculation_type", models.CharField(max_length=255)),
                ("value", models.FloatField()),
                (
                    "billing_period",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rodManager.billingperiod",
                    ),
                ),
            ],
        ),
    ]