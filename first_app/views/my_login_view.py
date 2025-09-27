from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()












def my_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Role’a göre yönlendirme
            if user.role == 'admin':
                return redirect('dashboard')
            elif user.role == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('dietitian_dashboard')  # artık çalışacak
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'my_login.html')




