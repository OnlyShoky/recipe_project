import factory
from faker import Faker
from PIL import Image
import io
import random
from recipes.models import Recipe  # Assuming your Recipe model is in the 'recipes' app

fake = Faker()

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    # Assuming Recipe model has these fields; adjust accordingly
    title = factory.LazyAttribute(lambda _: fake.word())  # Generates a random word as the name
    description = factory.LazyAttribute(lambda _: fake.sentence())  # Random sentence as description
    instructions = factory.LazyAttribute(lambda _: fake.paragraph())  # Random paragraph for instructions
    ingredients = factory.LazyAttribute(lambda _: fake.paragraph())  # Random paragraph for instructions

    # Generate a random image for the Recipe model
    @factory.lazy_attribute
    def image(self):
        # Create a random image using Pillow
        img = Image.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # Save the image to a BytesIO object to simulate a file
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        
        # Return the image as a Django File
        from django.core.files import File
        return File(img_io, name=f'{self.title}_image.jpg')
