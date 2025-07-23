from django.urls import path
from django.contrib import admin
from recipes import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from ingredients.views import IngredientAPIView, IngredientDetailAPIView
from recipes.views import RecipeAPIView, RecipeDetailAPIView, RecipeSearchAPIView ,contact_view, faq_view, about_view,preepweek_view, generate_random_meals

# Registering API routes with the DefaultRouter if needed
router = routers.DefaultRouter()

# The DefaultRouter will automatically generate URLs for viewsets if you use them
# urlpatterns = router.urls

# Frontend and API routes
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ### Frontend Routes ###
    path('', views.home, name='home'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('about/', about_view, name='about'),
    
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<uuid:id>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search_recipes, name='search_recipes'),
    
    path('preepweek/', preepweek_view, name='preepweek'),
    
    # ### Frontend function Routes ###
    path('generate-meals/', generate_random_meals, name='generate_meals'),
    
    
    # ### Backend Routes ###
    path('api/v1/', include(router.urls)),
    # ### Ingredient API Routes ###
    path('api/ingredients/', IngredientAPIView.as_view(), name='ingredient-list'),
    path('api/ingredients/<uuid:id>/', IngredientDetailAPIView.as_view(), name='ingredient-detail'),
    
    # ### Recipe API Routes ###
    # URL to fetch the last 5 recipes
    path('api/v1/recipes/', RecipeAPIView.as_view(), name='recipe-list'),
    path('api/v1/recipes', RecipeSearchAPIView.as_view(), name='recipe-search'),
    
    # URL to fetch a single recipe by ID
    path('api/v1/recipes/<uuid:id>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    