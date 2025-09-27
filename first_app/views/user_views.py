from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
def home_redirect(request):
    # Boş URL’ye yönlendirme
    if request.user.role == 'admin':
        return redirect('user_list')
    else:
        return redirect('dashboard')


# Admin panel view’ları
@login_required
def user_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
def user_add(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email')
        password = request.POST['password']
        role = request.POST['role']
        User.objects.create_user(username=username, password=password, role=role,email=email)
        return redirect('user_list')
    return render(request, 'admin/user_add.html')

def user_edit(request, pk):
    editing_user = get_object_or_404(User, pk=pk)
    ROLE_CHOICES = User.ROLE_CHOICES

    if request.method == 'POST':
        editing_user.username = request.POST.get('username', editing_user.username)
        editing_user.email = request.POST.get('email', editing_user.email)
        editing_user.first_name = request.POST.get('first_name', editing_user.first_name)
        editing_user.last_name = request.POST.get('last_name', editing_user.last_name)
        editing_user.role = request.POST.get('role', editing_user.role)
        editing_user.is_active = request.POST.get('is_active') == '1'
        editing_user.save()
        return redirect('user_list')

    context = {
        'editing_user': editing_user,
        'ROLE_CHOICES': ROLE_CHOICES,
    }
    return render(request, 'admin/user_edit.html', context)



@login_required
def user_delete(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    
    user_to_delete = User.objects.get(pk=pk)
    
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('user_list')
    
    return render(request, 'admin/user_delete.html', {'user_to_delete': user_to_delete})





import requests
from django.http import JsonResponse
from ..models import User, CustomerData
from django.db.models import Count
from datetime import datetime, timedelta

def fetch_customers_view(request):
    url = "https://dummyjson.com/users"
    try:
        response = requests.get(url)
        data = response.json()

        for item in data.get("users", []):  # users yoksa boş liste ile çalışır
            # User kaydı oluştur veya güncelle
            user, _ = User.objects.update_or_create(
                username=item["username"],
                defaults={
                    "role": "patient",
                    "email": item.get("email", ""),
                }
            )

            # CustomerData kaydı oluştur veya güncelle
            CustomerData.objects.update_or_create(
                user=user,
                defaults={
                    "age": item.get("age", None),
                    "gender": item.get("gender", None),
                    "height_cm": float(item.get("height", 0)),
                    "weight_kg": float(item.get("weight", 0)),
                    "waist_cm": None,
                    "nutrition_score": None,
                }
            )

        return JsonResponse({"status": "success", "message": "Customers updated successfully"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})




from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
from ..models import User

def user_stats(request):
    # Şu anki zamanı timezone-aware olarak al
    now = timezone.now()
    
    # Temel istatistikler
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Son 7 gündeki yeni kayıtlar (timezone-aware)
    new_users = User.objects.filter(
        date_joined__gte=now-timedelta(days=7)
    ).count()
    
    # Son 24 saatte giriş yapanlar (timezone-aware)
    recent_logins = User.objects.filter(
        last_login__gte=now-timedelta(days=1)
    ).count()
    
    # Son 30 günlük kayıt istatistikleri (timezone-aware)
    registration_dates = []
    registration_counts = []
    
    for i in range(30, -1, -1):
        date = now - timedelta(days=i)
        date_str = date.strftime('%d %b')
        count = User.objects.filter(
            date_joined__date=date.date()  # date() metodu timezone'u korur
        ).count()
        
        registration_dates.append(date_str)
        registration_counts.append(count)
    
    # Rol dağılımı
    roles = User.objects.values('role').annotate(count=Count('role')).order_by('-count')
    role_labels = [r['role'] for r in roles]
    role_values = [r['count'] for r in roles]
    
    # Aktivite verileri (son 30 gün) (timezone-aware)
    activity_labels = []
    login_counts = []
    registration_counts_act = []
    
    for i in range(30, -1, -1):
        date = now - timedelta(days=i)
        date_str = date.strftime('%d %b')
        activity_labels.append(date_str)
        
        login_count = User.objects.filter(
            last_login__date=date.date()  # date() metodu timezone'u korur
        ).count()
        login_counts.append(login_count)
        
        reg_count = User.objects.filter(
            date_joined__date=date.date()  # date() metodu timezone'u korur
        ).count()
        registration_counts_act.append(reg_count)
    
    return JsonResponse({
        'status': 'success',
        'total_users': total_users,
        'active_users': active_users,
        'new_users': new_users,
        'recent_logins': recent_logins,
        'registration_dates': registration_dates,
        'registration_counts': registration_counts,
        'roles': {
            'labels': role_labels,
            'values': role_values
        },
        'activity': {
            'labels': activity_labels,
            'logins': login_counts,
            'registrations': registration_counts_act
        }
    })