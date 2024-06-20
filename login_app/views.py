from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse 
from .forms import UserLoginForm, UserRegistrationForm, CustomUserUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


def start_page(request):
    return render(request, "registration/front_page.html")

def home(request):
    return render(request, "registration/home.html")

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'User logged in successfully')
                # Generating JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response = redirect('dashboard')
                response.set_cookie('jwt', access_token)
                return response
            else:
                messages.error(request, 'Credentials are not correct')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'User logged out successfully')
    response = redirect('login')  # Redirect to login page or any other page
    response.delete_cookie('jwt')  # Delete the JWT token from cookies
    return response

# <a href="{% url 'logout' %}" class="btn btn-danger">Logout</a>

def dashboard_view(request):
    return render(request, 'dashboard.html')



def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User registered successfully')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

from .models import CustomUser

def user_list(request):
    users_list = CustomUser.objects.all()
    return render(request, 'registration/user_list.html', {'users_list':users_list})


def delete_user(request, pk):
    delete_user = CustomUser.objects.get(id=pk)
    delete_user.delete()
    return redirect('/user_list')


@login_required
def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/user_list', pk=pk)  # Adjust the redirect as per your URL pattern
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'registration/update_user.html', {'form': form, 'user': user})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GrantPermissionForm
from .models import CustomUser

def superuser_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Only superusers can access this page.')
            return redirect('home')  # Adjust this to the appropriate home URL name
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@login_required
@superuser_required
def grant_permissions_view(request):
    if request.method == 'POST':
        form = GrantPermissionForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            make_superuser = form.cleaned_data['make_superuser']
            make_staff = form.cleaned_data['make_staff']
            permissions = form.cleaned_data['permissions']

            user = get_object_or_404(CustomUser, id=user_id)

            user.is_superuser = make_superuser
            user.is_staff = make_staff
            user.user_permissions.set(permissions)
            user.save()

            messages.success(request, f'Permissions updated for {user.full_name}')
            return redirect('grant_permissions')
    else:
        form = GrantPermissionForm()

    users = CustomUser.objects.all()
    return render(request, 'registration/grant_permissions.html', {'form': form, 'users': users})
