from django.urls import path
from .views import RecipeList, CreateRecipe, UpdateRecipe, ViewRecipe, DeleteRecipe, LoginPage, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', RecipeList.as_view(), name='recipeList'),
    path('create/', CreateRecipe.as_view(), name='create'),
    path('view/<int:pk>/', ViewRecipe.as_view(), name='view'),
    path('update/<int:pk>/', UpdateRecipe.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteRecipe.as_view(), name='delete'),
]