from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from recipes.models import Recipe  # Assuming your Recipe model is in the 'recipes' app


class RecipeTestCase(APITestCase):
    """
    Test suite for Recipe
    """
    def setUp(self):
        self.client = APIClient()
        self.recipe_data = {
            "title": "Test Recipe",
            "description": "This is a test recipe description.",
            "ingredients": "Sugar, flour, eggs",
            "instructions": "Mix ingredients and bake for 20 minutes.",
            "status": 1,  # Assuming 1 is 'active'
            "activate_date": "2024-12-30T09:10:23.857753Z",
            "deactivate_date": None
        }
        self.url = "/recipes/"  # Assuming this is the correct endpoint for fetching recipes

        # Create a recipe in the database for the tests
        self.recipe = Recipe.objects.create(**self.recipe_data)

    def test_get_recipe_list(self):
        '''
        Test retrieving the list of recipes
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure that there is at least one recipe in the response

    def test_get_recipe_by_id(self):
        '''
        Test retrieving a recipe by its ID
        '''
        response = self.client.get(f"{self.url}{self.recipe.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.recipe.title)
        self.assertEqual(response.data['description'], self.recipe.description)

    def test_get_recipe_not_found(self):
        '''
        Test retrieving a non-existent recipe
        '''
        response = self.client.get(f"{self.url}9999/")  # Assuming 9999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_recipe_list_empty(self):
        '''
        Test retrieving an empty list of recipes when no recipes are created
        '''
        # Delete the created recipe to simulate an empty list
        self.recipe.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Ensure that the list is empty
        
    def test_throttling(self):
        '''
        Test the API throttling limit of 50 requests per minute
        '''
        # Make 50 successful requests
        for i in range(50):
            response = self.client.get(self.url)

        # The 51st request should return a 429 Too Many Requests error
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # Optionally, check the Retry-After header if your throttling includes it
        retry_after = response.headers.get('Retry-After')
        self.assertIsNotNone(retry_after)  # Ensure the Retry-After header is present
        
        

