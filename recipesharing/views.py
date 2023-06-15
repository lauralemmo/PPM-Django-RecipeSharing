from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from recipesharing.forms import RecipeForm
from recipesharing.models import Recipe, Favorite


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect a una pagina dopo il login
        else:
            error_message = 'Credenziali non valide. Riprova.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


@login_required
def userLogout(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def createRecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('recipeDetail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    context = {'form': form}
    return render(request, 'recipe/create.html', context)


def recipeDetail(request, recipe_id):
    # Logica per ottenere i dettagli della ricetta con l'ID specificato
    recipe = Recipe.objects.get(id=recipe_id)
    is_favorite = False
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    context = {
        'recipe': recipe,
        'is_favorite': is_favorite,
        'is_authenticated': is_authenticated
    }
    return render(request, 'recipe/detail.html', context)


@login_required
def recipeDetailFavorite(request, recipe_id):
    # Logica per ottenere i dettagli della ricetta con l'ID specificato
    recipe = Recipe.objects.get(id=recipe_id)
    is_favorite = False
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    context = {
        'recipe': recipe,
        'is_favorite': is_favorite,
        'is_authenticated': is_authenticated
    }
    return render(request, 'recipe/detailFavorite.html', context)


def getAppetizersByTitle(request):
    if request.method == 'GET':
        searchQuery = request.GET.get('query', '')
        if(searchQuery == "all"):
            recipes = Recipe.objects.filter(title__icontains="", category="APPETIZER")
            return render(request, 'category/appetizers.html', {'recipes': recipes, 'searchAllQuery': searchQuery})
        else:
            recipes = Recipe.objects.filter(title__icontains=searchQuery, category="APPETIZER")
            return render(request, 'category/appetizers.html', {'recipes': recipes, 'searchByTitleQuery': searchQuery})


def getFirstsByTitle(request):
    if request.method == 'GET':
        searchQuery = request.GET.get('query', '')
        if(searchQuery == "all"):
            recipes = Recipe.objects.filter(title__icontains="", category="FIRST")
            return render(request, 'category/firsts.html', {'recipes': recipes, 'searchAllQuery': searchQuery})
        else:
            recipes = Recipe.objects.filter(title__icontains=searchQuery, category="FIRST")
            return render(request, 'category/firsts.html', {'recipes': recipes, 'searchByTitleQuery': searchQuery})


def getSecondsByTitle(request):
    if request.method == 'GET':
        searchQuery = request.GET.get('query', '')
        if(searchQuery == "all"):
            recipes = Recipe.objects.filter(title__icontains="", category="SECOND")
            return render(request, 'category/seconds.html', {'recipes': recipes, 'searchAllQuery': searchQuery})
        else:
            recipes = Recipe.objects.filter(title__icontains=searchQuery, category="SECOND")
            return render(request, 'category/seconds.html', {'recipes': recipes, 'searchByTitleQuery': searchQuery})


def getSidesByTitle(request):
    if request.method == 'GET':
        searchQuery = request.GET.get('query', '')
        if(searchQuery == "all"):
            recipes = Recipe.objects.filter(title__icontains="", category="SIDE")
            return render(request, 'category/sides.html', {'recipes': recipes, 'searchAllQuery': searchQuery})
        else:
            recipes = Recipe.objects.filter(title__icontains=searchQuery, category="SIDE")
            return render(request, 'category/sides.html', {'recipes': recipes, 'searchByTitleQuery': searchQuery})


def getDessertsByTitle(request):
    if request.method == 'GET':
        searchQuery = request.GET.get('query', '')
        if(searchQuery == "all"):
            recipes = Recipe.objects.filter(title__icontains="", category="DESSERT")
            return render(request, 'category/desserts.html', {'recipes': recipes, 'searchAllQuery': searchQuery})
        else:
            recipes = Recipe.objects.filter(title__icontains=searchQuery, category="DESSERT")
            return render(request, 'category/desserts.html', {'recipes': recipes, 'searchByTitleQuery': searchQuery})

@login_required
def addToFavorites(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    Favorite.objects.create(user=request.user, recipe=recipe)
    is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    context = {
        'recipe': recipe,
        'is_favorite': is_favorite
    }
    #return render(request, 'recipe/detail.html', context)
    return recipeDetail(request, recipe_id)


@login_required
def getAllFavorites(request):
    userFavorites = Favorite.objects.filter(user=request.user)
    context = {
        'user_favorites': userFavorites
    }
    return render(request, 'favorites.html', context)


@login_required
def removeFavorite(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user_id = request.POST.get('user_id')
        favorite = get_object_or_404(Favorite, recipe_id=recipe_id, user_id=user_id)

        # Verifica se l'utente corrente è autorizzato a eliminare il preferito
        if favorite.user == request.user:
            favorite.delete()
    return redirect('getAllFavorites')


@login_required
def removeFavoriteFromView(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        user_id = request.POST.get('user_id')
        favorite = get_object_or_404(Favorite, recipe_id=recipe_id, user_id=user_id)

        # Verifica se l'utente corrente è autorizzato a eliminare il preferito
        if favorite.user == request.user:
            favorite.delete()
        return recipeDetail(request, recipe_id)


@login_required
def getMyRecipes(request):
    if request.user.is_authenticated:
        userRecipes = Recipe.objects.filter(user=request.user)
    else:
        userRecipes = []

    context = {
        'user_recipes': userRecipes
    }

    return render(request, 'my_recipes.html', context)


@login_required
def removeRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Verifica se l'utente corrente è autorizzato a rimuovere la ricetta
    if recipe.user == request.user:
        recipe.delete()

    return getMyRecipes(request)


@login_required
def updateRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # se ho cliccato salva sul form di modifica (altrimenti renderizzo solamente il form con i dati della ricetta)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return getMyRecipes(request)

    context = {
        'recipe': recipe
    }
    return render(request, 'recipe/update.html', context)


