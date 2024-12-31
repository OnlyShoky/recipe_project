from django.urls import path
from django.contrib import admin
from recipes import views
from rest_framework import routers
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings





router = routers.DefaultRouter()

urlpatterns = router.urls


urlpatterns += [
    path('admin/', admin.site.urls),
    
    
    ### Frontend ###
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<uuid:id>/', views.recipe_detail, name='recipe_detail'),
    
    ### API ###
    # URL to fetch the last 5 recipes
    path('api/recipes/', views.RecipeAPIView.as_view(), name='recipe-list'),
    
    # URL to fetch a single recipe by ID
    path('api/recipes/<uuid:id>/', views.RecipeDetailAPIView.as_view(), name='recipe-detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)