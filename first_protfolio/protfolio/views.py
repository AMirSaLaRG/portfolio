from django.shortcuts import render, HttpResponse, redirect
from .models import Project, Skill, Course, ProjectSkill, ContactMessage
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .forms import ContactForm
from django.contrib import messages
import time


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
    context = {
        'projects': Project.objects.all(),
        'skills': Skill.objects.all(),
        'projectskills': ProjectSkill.objects.all().order_by('-project_id')
    }

    return render(request, 'protfolio/projects.html', context)

def project_detail(request, project_id):
    # Fetch the project using the provided project_id
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)

    context = {
        'project': project,
        'skills': Skill.objects.all(),
        'projectskills': ProjectSkill.objects.filter(project=project).order_by('-project_id')
    }
    return render(request, 'protfolio/project_detail.html', context)

def contact(request):
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        # Check if the IP address is blocked
        if cache.get(f'blocked_(ip)'):
            # If the IP address is blocked, return a forbidden response
            return HttpResponseForbidden("Too many submissions. Try again later.")
        # Track submisions (count + timestamp)
        submission = cache.get(f'submission_{ip}', [])

        #Remove submission older than 1 minute
        curret_time = time.time()
        submission = [s for s in submission if curret_time - s < 60]
        
        if len(submission) >= 3:
            # Block the IP address for 1 minute
            cache.set(f'blocked_{ip}', True, timeout=60)
            return HttpResponseForbidden("Too many submissions. Try again later.")
        # Add the current submission timestamp to the list  
        submission.append(curret_time)
        # Save the updated submission list back to the cache
        cache.set(f'submission_{ip}', submission, timeout=60)
        # Process the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        contact_message = ContactMessage(name=name, email=email,phone=phone, message=message)
        contact_message.save()
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    else:
        pass
    # Handle GET request here if needed
    form = ContactForm() 
    return render(request, 'protfolio/contact.html' , {'form': form})

def about(request):
    context = {
        'skills': Skill.objects.all(),
        'courses': Course.objects.all().order_by('-completion_date')[:5],
        'projectskills': ProjectSkill.objects.all().order_by('-project_id')
    }
    
    return render(request, 'protfolio/about.html', context)

def blog(request):
    return render(request, 'protfolio/blog.html')