from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def home(request):
    return redirect('/register/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            return redirect('/register/')

        return HttpResponse("Login yoki parol xato")

    return render(request, 'core/login.html')

from .models import Competition
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render
from .models import Competition, Participant

from django.shortcuts import render
from .models import Competition, Participant


def register(request):
    competitions = Competition.objects.all()

    if request.method == 'POST':
        competition = Competition.objects.get(key=request.POST['competition'])

        # 🔢 NECHTA ISHTIROKCHI BOR?
        count = Participant.objects.filter(competition=competition).count()

        # 🤖 AVTOMATIK KOD
        code = f"{competition.key}{count + 1}"

        Participant.objects.create(
            competition=competition,
            code=code,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            region=request.POST['region'],
            district=request.POST['district'],
            phone=request.POST['phone'],
        )

        return render(request, 'core/register.html', {
            'competitions': competitions,
            'success': f"✅ Ro‘yxatdan o‘tildi. Sizning kodingiz: {code}"
        })

    return render(request, 'core/register.html', {
        'competitions': competitions
    })

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # 👈 faqat admin
    path('', include('core.urls')),
]



