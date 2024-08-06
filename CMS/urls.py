"""
URL configuration for CMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from service import views
from rest_framework.routers import DefaultRouter
from CMS.views import NoticeViewSet
from service.views import LoginAPIView

router = DefaultRouter()
router.register(r'NO', NoticeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ApiOverview, name='index'),
    path('logout', views.custom_logout, name='logout'),
    path('api/v1/login/', LoginAPIView.as_view(), name = 'login'),
    path('Create/', views.AddNotice, name= 'AddNotice'),
    path('Update/<str:pk>', views.UpdateNotice, name= 'UpdateNotice'),
    path('Delete/<str:pk>', views.NoticeDelete, name= 'NoticeDelete'),
    path('NoticeList/', views.NoticeList, name= 'NoticeList'),
    path('view/', views.view_items, name= 'view'),
    path('AddUser/', views.AddUser.as_view(), name = 'AddUser'),
    path('', include(router.urls))

]
