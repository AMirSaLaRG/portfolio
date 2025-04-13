from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    # template = "index.html"
    # context = ""
    # return render(request, template, context)
    # return HttpResponse("Hellow world")
    return render(request, 'protfolio/index.html')

def projects(request):
    return render(request, 'protfolio/projects.html')

def contact(request):
    return render(request, 'protfolio/contact.html')

def about(request):
    return render(request, 'protfolio/about.html')

def blog(request):
    return render(request, 'protfolio/blog.html')