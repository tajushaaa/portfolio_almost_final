from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("project/create/", views.create_project, name="create_project"),
    path('project/<slug:project_slug>/edit/',
         views.edit_project, name='edit_project'),
    path('delete_project/', views.delete_project, name='delete_project'),
    path("project/<slug:project_slug>/",
         views.project_detail, name="project_detail"),
    path("project/<slug:project_slug>/add_image/",
         views.add_image, name="add_image"),
    path('logout/', views.custom_logout, name='custom_logout'),
]

urlpatterns += staticfiles_urlpatterns()
