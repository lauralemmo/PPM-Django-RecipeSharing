from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.userLogin, name="login"),
    path("logout", views.userLogout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("recipe/create", views.createRecipe, name="createRecipe"),
    path("recipe/<int:recipe_id>", views.recipeDetail, name="recipeDetail"),
    path("recipeFavorite/<int:recipe_id>", views.recipeDetailFavorite, name="recipeDetailFavorite"),

    path('category/appetizers', views.getAppetizersByTitle, name='getAppetizersByTitle'),
    path('category/firsts', views.getFirstsByTitle, name='getFirstsByTitle'),
    path('category/seconds', views.getSecondsByTitle, name='getSecondsByTitle'),
    path('category/sides', views.getSidesByTitle, name='getSidesByTitle'),
    path('category/desserts', views.getDessertsByTitle, name='getDessertsByTitle'),

    path('recipe/<int:recipe_id>/addToFavorites/', views.addToFavorites, name='addToFavorites'),

    path('favorites', views.getAllFavorites, name='getAllFavorites'),
    path('removeFavorite', views.removeFavorite, name='removeFavorite'),
    path('removeFavoriteFromView', views.removeFavoriteFromView, name='removeFavoriteFromView'),
    path('getMyRecipes', views.getMyRecipes, name='getMyRecipes'),
    path('removeRecipe/<int:recipe_id>', views.removeRecipe, name='removeRecipe'),
    path('recipe/update/<int:recipe_id>', views.updateRecipe, name='updateRecipe'),
]