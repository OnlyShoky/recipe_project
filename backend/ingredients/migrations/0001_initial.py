# Generated by Django 4.1.3 on 2025-01-01 09:40

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NutritionalTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "calories",
                    models.FloatField(
                        blank=True, help_text="Calories per serving (kcal)", null=True
                    ),
                ),
                (
                    "carbohydrates",
                    models.FloatField(
                        blank=True, help_text="Total carbohydrates (g)", null=True
                    ),
                ),
                (
                    "protein",
                    models.FloatField(
                        blank=True, help_text="Protein content (g)", null=True
                    ),
                ),
                (
                    "fat",
                    models.FloatField(blank=True, help_text="Total fat (g)", null=True),
                ),
                (
                    "saturated_fat",
                    models.FloatField(
                        blank=True, help_text="Saturated fat (g)", null=True
                    ),
                ),
                (
                    "trans_fat",
                    models.FloatField(blank=True, help_text="Trans fat (g)", null=True),
                ),
                (
                    "fiber",
                    models.FloatField(
                        blank=True, help_text="Dietary fiber (g)", null=True
                    ),
                ),
                (
                    "sugar",
                    models.FloatField(
                        blank=True, help_text="Total sugars (g)", null=True
                    ),
                ),
                (
                    "sodium",
                    models.FloatField(
                        blank=True, help_text="Sodium content (mg)", null=True
                    ),
                ),
                (
                    "cholesterol",
                    models.FloatField(
                        blank=True, help_text="Cholesterol (mg)", null=True
                    ),
                ),
                (
                    "potassium",
                    models.FloatField(
                        blank=True, help_text="Potassium (mg)", null=True
                    ),
                ),
                (
                    "vitamin_a",
                    models.FloatField(
                        blank=True, help_text="Vitamin A (IU)", null=True
                    ),
                ),
                (
                    "vitamin_c",
                    models.FloatField(
                        blank=True, help_text="Vitamin C (mg)", null=True
                    ),
                ),
                (
                    "calcium",
                    models.FloatField(blank=True, help_text="Calcium (mg)", null=True),
                ),
                (
                    "iron",
                    models.FloatField(blank=True, help_text="Iron (mg)", null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Inactive"), (1, "Active")],
                        default=1,
                        verbose_name="status",
                    ),
                ),
                (
                    "activate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for an immediate activation",
                        null=True,
                    ),
                ),
                (
                    "deactivate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for indefinite activation",
                        null=True,
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "nutrition",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ingredients.nutritionaltable",
                    ),
                ),
            ],
            options={"get_latest_by": "modified", "abstract": False,},
        ),
    ]
