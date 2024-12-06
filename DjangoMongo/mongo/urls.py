from django.urls import path
from . import views
from .views import add_person

urlpatterns = [
    path('',views.index),
    path('add/',add_person),
    path('show/',views.get_all_person),

]