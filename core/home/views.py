from django.shortcuts import render

from .models import Recipe
from django.http import HttpResponse , JsonResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



@login_required(login_url='/login/')

def recipes(request):
    if request.method == "POST"
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        Recipe.objects.create(
            day = 'day',
            name = 'name',
            description = 'description',

        )
        return redirect('/')
     
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            day_icontains = request.GET.get('search')
        )
    context = {'recipes':queryset}
    return render(request, 'recipe.html',context)



        