# Generated by Django 4.1.3 on 2025-01-21 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0003_ingredient_related_recipe"),
        ("recipes", "0010_alter_course_options_alter_cuisine_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="nutrition",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ingredients.nutritionaltable",
            ),
        ),
    ]
