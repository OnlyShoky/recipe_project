from django.urls import path
from django.contrib import admin
from recipes.views import RecipeAPIView, RecipeDetailAPIView
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = router.urls


urlpatterns += [
    path('admin/', admin.site.urls),
    # URL to fetch the last 5 recipes
    path('recipes/', RecipeAPIView.as_view(), name='recipe-list'),
    
    # URL to fetch a single recipe by ID
    path('recipes/<uuid:id>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
]