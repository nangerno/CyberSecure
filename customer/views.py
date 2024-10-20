from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    title = 'Home'
    return render(request, 'customer/index.html',{'title': title})  # You can customize the template name and path
'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('customer:index')  # Redirect to the index page after successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'registration/login.html',{'title': 'Logins'})  # Replace 'registration/login.html' with your login template path
'''

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('customer:index')  # Redirect to the index page after successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    # Render the login page with error messages
    return render(request, 'registration/login.html', {'title': 'Logins'})

@login_required
def some_protected_view(request):
    return render(request, 'customer/protected.html')  # Example of a protected view accessible only to logged-in users
