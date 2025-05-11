from django.urls import path, include


from . import views

appname = "protfolio"
urlpatterns = [
    path("", views.index, name="home"),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('animate-project/', views.animate_project, name='animate_project'),
    path('animate-project/btn', views.animate_buttons, name='animate_buttons'),
    path('animate-project/btn-group', views.animate_buttons_group, name='animate_buttons_group'),
    path('animate-project/img', views.animate_img, name='animate_img'),
    path('animate-project/card', views.animate_cards, name='animate_cards'),
]
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher endpoint
]