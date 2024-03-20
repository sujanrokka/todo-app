from django.urls import path
from . import views
urlpatterns=[
    path('create/',views.create,name='create'),
    path('retrieve/',views.retrieve,name= 'retrieve'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('register/',views.register,name= "register"),
    path('login/',views.loginn,name= "login"),
    path('logout/',views.logoutt,name="logout"),
]