from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cocktail



class LoginPage(LoginView):
    template_name = 'recipes/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('recipeList')


class RegisterPage(FormView):
    template_name = 'recipes/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('RecipeList')

    def form_valid(self, form):
        user = form.save()
        if  user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('recipes_list')
        return super(RegisterPage, self).get(*args, **kwargs)


class RecipeList(LoginRequiredMixin, ListView):
    model = Cocktail
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes_list'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['recipes_list'] = contex['recipes_list'].filter(user = self.request.user)

        search_input = self.request.GET.get('search-area') or  ''
        if search_input:
            contex['recipes_list'] = contex['recipes_list'].filter(name__icontains = search_input)
        contex['search_input'] = search_input

        return contex


#CRUD functions
class CreateRecipe(LoginRequiredMixin, CreateView):
    model = Cocktail
    template_name = 'recipes/cocktail_form.html'
    fields = ['name', 'ingredients', 'instructions']
    success_url = reverse_lazy('recipeList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateRecipe, self).form_valid(form)


class ViewRecipe(LoginRequiredMixin, DetailView):
    model = Cocktail
    template_name = 'recipes/cocktail.html'
    success_url = reverse_lazy('recipeList')


class UpdateRecipe(LoginRequiredMixin, UpdateView):
    model = Cocktail
    fields = ['name', 'ingredients', 'instructions']
    success_url = reverse_lazy('recipeList')


class DeleteRecipe(LoginRequiredMixin, DeleteView):
    model = Cocktail
    template_name = 'recipes/confirm_delete.html'
    success_url = reverse_lazy('recipeList')
