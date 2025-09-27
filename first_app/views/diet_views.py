from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import CustomerData, User, DietPlan, Message,Food,MealLog
from django.contrib.auth import get_user_model


User = get_user_model()
   

@login_required
def diet_plan_list(request):
    role = getattr(request.user, 'role', '')

    if role == 'patient':
        
        plans = DietPlan.objects.filter(patient=request.user)
        meals = MealLog.objects.filter(user=request.user)
        customer = CustomerData.objects.filter(user=request.user).first()
        my_bmi = round(customer.bmi(), 2) if customer else 0
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()

        context = {
            'plans': plans,
            'meals': meals,
            'my_bmi': my_bmi,
            'total_messages': total_messages,
            'messages': inbox_messages,
            'sent': sent_messages,
        }
        return render(request, 'dietitian/diet_plan_list.html', context)

    elif role == 'dietitian':
        
        plans = DietPlan.objects.all()
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
            'plans': plans,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
            'total_messages': total_messages,
            'customers': customers,
        }

        return render(request, 'dietitian/diet_plan_list.html', context)

    else:
        
        return redirect('home')

@login_required
def diet_plan_add(request):
    
    if request.user.role != 'dietitian':
         return redirect('dashboard')

 
    patients = User.objects.filter(role='patient')

  
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
       
        DietPlan.objects.create(
            dietitian=request.user,
            patient_id=request.POST['patient'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            description=request.POST['description']
        )
        return redirect('diet_plan_list')

    context = {
        'patients': patients,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'dietitian/diet_plan_add.html', context)


@login_required
def diet_plan_edit(request, pk):
   
    if request.user.role != 'dietitian':
        return redirect('dashboard')

   
    plan = get_object_or_404(DietPlan, pk=pk)
    patients = User.objects.filter(role='patient')

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
       
        plan.patient_id = request.POST.get('patient')
        plan.start_date = request.POST.get('start_date')
        plan.end_date = request.POST.get('end_date')
        plan.description = request.POST.get('description')
        plan.save()
        return redirect('diet_plan_list')

    context = {
        'plan': plan,
        'patients': patients,
        'dietitian_name': plan.dietitian.username,  
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'dietitian/diet_plan_edit.html', context)

@login_required
def diet_plan_delete(request, pk):
    plan = get_object_or_404(DietPlan, pk=pk)

    if request.user.role != 'dietitian':
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
        plan.delete()  
        return redirect('diet_plan_list')

    context = {
        'plan': plan,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'dietitian/diet_plan_delete.html', context)

