from django.shortcuts import render, HttpResponse
from .models import Project, Skill, Course, ProjectSkill
# Create your views here.

def index(request):
    context = {
        'projects': Project.objects.filter(featured=True)[:7],
        'skills': Skill.objects.filter(showcase=True),
        'courses': Course.objects.all().order_by('-completion_date')[:5],
        'projectskills': ProjectSkill.objects.all().order_by('-project_id')
    }
    return render(request, 'protfolio/index.html', context)

def projects(request):
    return render(request, 'protfolio/projects.html')

def contact(request):
    return render(request, 'protfolio/contact.html')

def about(request):
    return render(request, 'protfolio/about.html')

def blog(request):
    return render(request, 'protfolio/blog.html')