from django.contrib.auth import logout
from django.shortcuts import redirect

def my_logout_view(request):
    # Kullanıcıyı sistemden çıkar
    logout(request)
    # Çıkış sonrası login sayfasına yönlendir
    return redirect('mylogin')
