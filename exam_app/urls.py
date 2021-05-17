from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('newtrip', views.new_trip),
    path('create', views.create),
    path('<int:id>', views.view),
    path('<int:id>/edit', views.edit),
    path('<int:id>/update', views.update),
    path('<int:id>/join', views.join),
    path('<int:id>/cancel', views.cancel),
    path('<int:id>/remove', views.remove),
    path('<int:id>/destroy', views.destroy)
]