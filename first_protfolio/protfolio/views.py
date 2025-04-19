from django.shortcuts import render, HttpResponse
from .models import Project, Skill, Course, ProjectSkill, ContactMessage
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        contact_message = ContactMessage(name=name, email=email,phone=phone, message=message)
        contact_message.save()
        return HttpResponse("Thank you for your message!")
    else:
        pass
    # Handle GET request here if needed
   
    return render(request, 'protfolio/contact.html')

def about(request):
    return render(request, 'protfolio/about.html')

def blog(request):
    return render(request, 'protfolio/blog.html')