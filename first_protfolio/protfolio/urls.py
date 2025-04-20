from django.urls import path


from . import views

appname = "protfolio"
urlpatterns = [
    path("", views.index, name="home"),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
]
