from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from first_app.models import CustomerData, User
from first_app.forms import CustomerAddForm


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from ..models import DietPlan, CustomerData, Message, MealLog  


@login_required
def patient_dashboard(request):
    # Rol kontrolü
    if request.user.role != 'patient':
        return redirect('mylogin')  # role uyumsuzsa login sayfasına gönder

    # Hastanın kendi diyet planları
    plans = DietPlan.objects.filter(patient=request.user)

    # Hastanın kendi BMI bilgisi
    customer = CustomerData.objects.filter(user=request.user).first()
    my_bmi = round(customer.bmi(), 2) if customer else 0

    # Hastanın kendi yemek kayıtları
    meals = MealLog.objects.filter(user=request.user)

    # Mesajlar
    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()

    context = {
        'plans': plans,
        'my_bmi': my_bmi,
        'meals': meals,
        'total_messages': total_messages,
    }

    return render(request, 'patient/dashboard.html', context)




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from ..models import CustomerData, User, DietPlan, Message
from ..forms import CustomerAddForm
import requests
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth import get_user_model


User = get_user_model()  # it is  first_app.User


@login_required
def dietitian_dashboard(request):
    if request.user.role != 'dietitian':
        return redirect('mylogin')

    total_patients = User.objects.filter(role='patient').count()
    total_diet_plans = DietPlan.objects.count()
    customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
    total_bmi = 0
    count_bmi = 0
    for c in customers:
        bmi = c.bmi()
        if bmi is not None:
            total_bmi += bmi
            count_bmi += 1

        avg_bmi = round(total_bmi / count_bmi, 2) if count_bmi > 0 else 0
    
   
    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()
    context = {
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,    
       
    }

    return render(request, 'dietitian/dashboard.html', context)

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'patient':
            login(request, user)
            return redirect('patient_dashboard')
        else:
            error = "Invalid username or password"
            return render(request, 'my_login.html', {'error': error})
    return render(request, 'my_login.html')

@login_required
def customer_list(request):
   
    if request.user.role != 'dietitian':
        return redirect('dashboard')
    customers = CustomerData.objects.select_related('user').all()
    total_patients = User.objects.filter(role='patient').count()
    total_diet_plans = DietPlan.objects.count()
    bmi_customers = customers.exclude(weight_kg__isnull=True, height_cm__isnull=True)
    total_bmi = 0
    count_bmi = 0
    for c in bmi_customers:
        bmi = c.bmi()
        if bmi is not None:
            total_bmi += bmi
            count_bmi += 1
    avg_bmi = round(total_bmi / count_bmi, 2) if count_bmi > 0 else 0

  
    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()

    context = {
        'customers': customers,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'bmi_customers': bmi_customers,
    }

    return render(request, 'admin/customer_list.html', context)
@login_required
def customer_edit(request, pk):
 
    if not (request.user.is_superuser or request.user.role == 'dietitian'):
        return redirect('dashboard')
    
   
    customer = get_object_or_404(CustomerData, pk=pk)

  
    total_patients = User.objects.filter(role='patient').count()
    total_diet_plans = DietPlan.objects.count()

    customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
    total_bmi = 0
    count_bmi = 0
    for c in customers:
        bmi = c.bmi()
        if bmi is not None:
            total_bmi += bmi
            count_bmi += 1
    avg_bmi = round(total_bmi / count_bmi, 2) if count_bmi > 0 else 0

   
    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()

    if request.method == 'POST':
        form = CustomerAddForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerAddForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'admin/customer_edit.html', context)


@login_required
def customer_delete(request, pk):

    if not (request.user.is_superuser or request.user.role == 'dietitian'):
        return redirect('dashboard')

    customer = get_object_or_404(CustomerData, pk=pk)


    total_patients = User.objects.filter(role='patient').count()
    total_diet_plans = DietPlan.objects.count()

 
    customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
    total_bmi = 0
    count_bmi = 0
    for c in customers:
        bmi = c.bmi()
        if bmi is not None:
            total_bmi += bmi
            count_bmi += 1
    avg_bmi = round(total_bmi / count_bmi, 2) if count_bmi > 0 else 0


    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    context = {
        'customer': customer,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'admin/customer_delete.html', context)




@login_required
def customer_add(request):
    if not (request.user.is_superuser or request.user.role == 'dietitian'):
        return redirect('dashboard')

    total_patients = User.objects.filter(role='patient').count()
    total_diet_plans = DietPlan.objects.count()
    customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)

    total_bmi = 0
    count_bmi = 0
    for c in customers:
        bmi = c.bmi()
        if bmi is not None:
            total_bmi += bmi
            count_bmi += 1
    avg_bmi = round(total_bmi / count_bmi, 2) if count_bmi > 0 else 0

    inbox_messages = Message.objects.filter(receiver=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    total_messages = inbox_messages.count() + sent_messages.count()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        age = request.POST.get('age') or None
        gender = request.POST.get('gender') or None
        height_cm = float(request.POST.get('height_cm')) if request.POST.get('height_cm') else None
        weight_kg = float(request.POST.get('weight_kg')) if request.POST.get('weight_kg') else None
        waist_cm = float(request.POST.get('waist_cm')) if request.POST.get('waist_cm') else None
        nutrition_score = float(request.POST.get('nutrition_score')) if request.POST.get('nutrition_score') else None

        try:
         user = User(username=username, email=email, role='patient')
         user.set_password(password)
         user.save()
         print("Saved user with id:", user.id)
        except Exception as e:
         print("Error saving user:", e)

        CustomerData.objects.create(
            user=user,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg,
            waist_cm=waist_cm,
            nutrition_score=nutrition_score
        )

        return redirect('customer_list')

    context = {
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'admin/customer_add.html', context)

    

def patient_registrations_trend(request):
    today = now().date()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]

    data = []
    for day in last_30_days:
        count = User.objects.filter(role="patient", date_joined__date=day).count()
        data.append(count)

    return JsonResponse({
        "labels": [day.strftime("%d %b") for day in last_30_days],
        "counts": data,
    })
def patient_activity_trend(request):
    today = now().date()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]

    data = []
    for day in last_30_days:
        count = Message.objects.filter(
            timestamp__date=day,  
            sender__role="patient"
        ).count()
        data.append(count)

    return JsonResponse({
        "labels": [day.strftime("%d %b") for day in last_30_days],
        "counts": data,
    })

def bmi_by_gender(request):
    males = CustomerData.objects.filter(user__role="patient", gender="male")
    females = CustomerData.objects.filter(user__role="patient", gender="female")

    def count_bmi_group(queryset):
        counts = {"underweight":0, "normal":0, "overweight":0, "obese":0}
        for c in queryset:
          
            bmi_value = c.bmi() if callable(getattr(c, "bmi", None)) else getattr(c, "bmi", None)
            if bmi_value is None:
                continue
            if bmi_value < 18.5:
                counts["underweight"] += 1
            elif bmi_value < 25:
                counts["normal"] += 1
            elif bmi_value < 30:
                counts["overweight"] += 1
            else:
                counts["obese"] += 1
        return counts

    data = {
        "male": count_bmi_group(males),
        "female": count_bmi_group(females),
    }
    return JsonResponse(data)


def bmi_by_age(request):
    customers = CustomerData.objects.filter(user__role="patient")

 
    age_groups = ["<20","20-29","30-39","40-49","50+"]
    counts = {g: {"underweight":0,"normal":0,"overweight":0,"obese":0} for g in age_groups}

   
    groups = {
        "<20": customers.filter(age__lt=20),
        "20-29": customers.filter(age__gte=20, age__lt=30),
        "30-39": customers.filter(age__gte=30, age__lt=40),
        "40-49": customers.filter(age__gte=40, age__lt=50),
        "50+": customers.filter(age__gte=50),
    }

    for g, qs in groups.items():
        for c in qs:
            bmi_value = c.bmi() if callable(getattr(c, "bmi", None)) else getattr(c, "bmi", None)
            if bmi_value is None:
                continue

            if bmi_value < 18.5:
                counts[g]["underweight"] += 1
            elif bmi_value < 25:
                counts[g]["normal"] += 1
            elif bmi_value < 30:
                counts[g]["overweight"] += 1
            else:
                counts[g]["obese"] += 1

    return JsonResponse({"age_groups": age_groups, "counts": counts})

@login_required
def total_messages_trend(request):
    today = now().date()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    counts = []
    for day in last_30_days:
        count = Message.objects.filter(
            timestamp__date=day  
        ).count()
        counts.append(count)
    return JsonResponse({'labels':[day.strftime('%d %b') for day in last_30_days], 'counts': counts})


def total_dietplans_trend(request):
    today = now().date()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]

    counts = []
    for day in last_30_days:
        count = DietPlan.objects.filter(
            start_date=day  
        ).count()
        counts.append(count)

    return JsonResponse({
        'labels': [day.strftime('%d %b') for day in last_30_days],
        'counts': counts
    })
