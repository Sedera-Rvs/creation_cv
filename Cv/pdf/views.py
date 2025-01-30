from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile, CVStatistics
from django.template.loader import get_template
import io
from django.conf import settings
import os
import base64
from django.db.models import Count, Sum
import json
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pathlib import Path


# Create your views here.
def index(request):
    return render(request, "pdf/resume.html")

@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie!')
            return redirect('acceuil')
        else:
            messages.error(request, 'Erreur dans le formulaire')
    else:
        form = UserCreationForm()
    return render(request, 'pdf/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    return render(request, 'pdf/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté')
    return redirect('acceuil')

@login_required
def formulaire(request):
    if request.method == "POST":
        name = request.POST.get("name")
        proffession = request.POST.get("proffession")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        birthday = request.POST.get("birthday")
        language = request.POST.get("language")
        hobbie = request.POST.get("hobbie")
        skill = request.POST.get("skill")
        experience = request.POST.get("experience")
        formation = request.POST.get("formation")
        image = request.FILES.get("image")
        theme = request.POST.get("theme", "classic")  # Valeur par défaut: classic

        donnees = Profile(
            user=request.user,
            name=name,
            proffession=proffession,
            email=email,
            phone=phone,
            address=address,
            birthday=birthday,
            language=language,
            hobbie=hobbie,
            skill=skill,
            experience=experience,
            formation=formation,
            image=image,
            theme=theme
        )
        donnees.save()

        return redirect('verification')
    return render(request, 'pdf/formulaire.html')

@login_required
def verification(request, id=None):
    if id:
        profile = Profile.objects.get(pk=id, user=request.user)
    else:
        profiles = Profile.objects.filter(user=request.user)[:1]
        if not profiles:
            return redirect('formulaire')
        profile = profiles[0]
    
    context = {
        'profile': profile,  # L'objet profile complet
        'name': profile.name,
        'proffession': profile.proffession,
        'email': profile.email,
        'phone': profile.phone,
        'address': profile.address,
        'birthday': profile.birthday,
        'language': profile.language,
        'hobbie': profile.hobbie,
        'skill': profile.skill,
        'experience': profile.experience,
        'formation': profile.formation,
        'image': profile.image
    }
    return render(request, "pdf/verification.html", context)


def generer(request, id):
    profile = Profile.objects.get(pk=id)
    
    # Enregistrer les statistiques
    CVStatistics.objects.create(
        downloads=1,
        profession_category=profile.proffession,
        language_used=profile.language
    )

    # Préparer le contexte avec l'image en base64 si elle existe
    context = {
        'profile': profile,  # Pour les thèmes
        'name': profile.name,
        'proffession': profile.proffession,
        'email': profile.email,
        'phone': profile.phone,
        'address': profile.address,
        'birthday': profile.birthday,
        'language': profile.language,
        'hobbie': profile.hobbie,
        'skill': profile.skill,
        'experience': profile.experience,
        'formation': profile.formation,
    }

    # Gérer l'image
    if profile.image:
        try:
            with default_storage.open(profile.image.name, 'rb') as img_file:
                image_data = img_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                context['image_base64'] = f"data:image/jpeg;base64,{image_base64}"
        except Exception as e:
            print(f"Erreur lors de la lecture de l'image : {str(e)}")

    # Générer le HTML
    html_string = render_to_string('pdf/generator.html', context)
    
    # Créer le PDF avec WeasyPrint
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    # Créer la réponse HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cv_{profile.name}.pdf"'
    
    return response


@login_required
def download(request):
    # Récupérer les dates depuis les paramètres GET
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    # Filtrer les CV de l'utilisateur connecté
    profiles = Profile.objects.filter(user=request.user)
    
    # Appliquer les filtres de date si présents
    if date_debut:
        profiles = profiles.filter(date_added__date__gte=date_debut)
    if date_fin:
        profiles = profiles.filter(date_added__date__lte=date_fin)
    
    context = {
        'profile': profiles,
        'date_debut': date_debut,
        'date_fin': date_fin
    }
    
    return render(request, 'pdf/download.html', context)

def statistics(request):
    # Statistiques générales
    total_cvs = Profile.objects.count()
    total_downloads = CVStatistics.objects.aggregate(total=Sum('downloads'))['total'] or 0
    
    # Statistiques par profession
    profession_stats = Profile.objects.values('proffession').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Statistiques par langue
    language_stats = Profile.objects.values('language').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Données pour les graphiques
    profession_labels = [item['proffession'] for item in profession_stats]
    profession_data = [item['count'] for item in profession_stats]
    
    context = {
        'total_cvs': total_cvs,
        'total_downloads': total_downloads,
        'profession_labels': json.dumps(profession_labels),
        'profession_data': json.dumps(profession_data),
        'language_stats': language_stats,
    }
    
    return render(request, 'pdf/statistics.html', context)