from django.urls import path
from django.contrib import admin
from recipes import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from ingredients.views import IngredientAPIView, IngredientDetailAPIView
from recipes.views import RecipeAPIView, RecipeDetailAPIView

# Registering API routes with the DefaultRouter if needed
router = routers.DefaultRouter()

# The DefaultRouter will automatically generate URLs for viewsets if you use them
# urlpatterns = router.urls

# Frontend and API routes
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ### Frontend Routes ###
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/cuisine/<str:cuisine_name>/', views.recipe_cuisine, name='recipe_cuisine'),
    path('recipes/<uuid:id>/', views.recipe_detail, name='recipe_detail'),
    
    
    # ### Backend Routes ###
    path('api/', include(router.urls)),
    # ### Ingredient API Routes ###
    path('api/ingredients/', IngredientAPIView.as_view(), name='ingredient-list'),
    path('api/ingredients/<uuid:id>/', IngredientDetailAPIView.as_view(), name='ingredient-detail'),
    
    # ### Recipe API Routes ###
    # URL to fetch the last 5 recipes
    path('api/recipes/', RecipeAPIView.as_view(), name='recipe-list'),
    
    # URL to fetch a single recipe by ID
    path('api/recipes/<uuid:id>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
