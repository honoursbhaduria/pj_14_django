from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.http import HttpResponse , JsonResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login , authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User


# create rcipes page 

@login_required(login_url='/login/')

def recipes(request):
    if request.method == "POST":
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        Recipe.objects.create(
            day = day,
            name = name,
            description = description,

        )
        return redirect('/')
     
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            day__icontains = request.GET.get('search')
        )
    context = {'recipes':queryset}
    return render(request, 'recipe.html',context)


# update the recipes data 

@login_required(login_url="/login/")

def update_recipe(request, id):
    #frist time useed 404 
    recipe = get_object_or_404(Recipe, id=id)
    
    if request.method == "POST":
        #got data
        day = request.POST.get('day')
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if not all([day, name, description]):
            messages.error(request, "All fields are required!")
            return render(request, 'update_recipe.html', {'recipe': recipe})
        
        #updated thing if all correct
        try:
           
            recipe.day = day
            recipe.name = name
            recipe.description = description
            recipe.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipes') 
            
        except Exception as e:
            messages.error(request, f"Error updating recipe: {str(e)}")
            return render(request, 'update_recipe.html', {'recipe': recipe})
    
    
    return render(request, 'update_recipe.html', {'recipe': recipe})

#delete the recipes data 

@login_required(login_url="/login/")
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect("/")


#login page for user 

def login_page(request):
    if request.method == "POST":
        try :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.error(request, "username not found ")
                return redirect("/login/")
            user_obj = authenticate(username = username  , password = password)
            if user_obj:
                login(request, user_obj)
                return redirect('recipes')
            
            messages.error(request,"wrong password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request , "something went wrong ")
            return redirect('/register/')
    return render(request , "login.html")
            

def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.error(request , "username is taken ")
                return redirect('/register/')
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request , "account created")
            return redirect('/login/')
        except Exception as e :
            messages.error(request , "something went wrong ")
            return redirect('/register/')
    return render(request, "register.html")

#logout function 
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def pdf(request):
    if request.method == "POST":
        data = request.POST
        day = data.get('day')

        name = data.get('name')
        description = data.get('description')

        Recipe.objects.create(
            day = day ,
            name = name,
            description = description,
        )
        return redirect('pdf')
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            day__icontains = request.GET.get('search')
        )
    context = {'recipes' : queryset}
    return render(request , "pdf.html" , context)

        