from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()

router.register(r"api/customuser", CustomUserViewSet, basename="customuser")

urlpatterns = [
    path('', start_page),
    path('home', home, name='home'),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/', register_view, name='register'),
    path('user_list', user_list),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
    path('update_user/<int:pk>/', update_user, name='update_user'),
    path('grant_permissions/', grant_permissions_view, name='grant_permissions'),
    path('api/customuser', CustomUserViewSet.as_view({'get': 'list'}), name='customuser_api')
    


]
urlpatterns += router.urls