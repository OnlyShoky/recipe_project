import factory
from faker import Faker
from recipes.models import Recipe  # Assuming your recipe model is in the 'recipes' app

fake = Faker()

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    # Assuming Recipe model has these fields; adjust accordingly
    title = factory.LazyAttribute(lambda _: fake.word())  # Generates a random word as the name
    description = factory.LazyAttribute(lambda _: fake.sentence())  # Random sentence as description
    instructions = factory.LazyAttribute(lambda _: fake.paragraph())  # Random paragraph for instructions
    ingredients = factory.LazyAttribute(lambda _: fake.paragraph())  # Random paragraph for instructions


