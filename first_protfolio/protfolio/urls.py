from django.urls import path


from . import views

appname = "protfolio"
urlpatterns = [
    path("", views.index, name="index")
]
