
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from ..models import Message, MealLog, DietPlan, CustomerData, Food,User

User = get_user_model()


def get_patient_context(user):
    
    plans = DietPlan.objects.filter(patient=user)
    customer = CustomerData.objects.filter(user=user).first()
    my_bmi = round(customer.bmi(), 2) if customer else 0
    inbox_messages = Message.objects.filter(receiver=user)
    sent_messages = Message.objects.filter(sender=user)
    total_messages = inbox_messages.count() + sent_messages.count()
    meals = MealLog.objects.filter(user=user)
    return {
        'plans': plans,
        'meals': meals,
        'my_bmi': my_bmi,
        'messages': inbox_messages,
        'sent': sent_messages,
        'total_messages': total_messages,
    }

@login_required
def meal_add(request):
    if getattr(request.user, 'role', '') != 'patient':
        return redirect('meal_list')
    foods = Food.objects.all()
    if request.method == 'POST':
        MealLog.objects.create(
            user=request.user,
            date=request.POST['date'],
            food_id=request.POST['food'],
            quantity=request.POST['quantity']
        )
        return redirect('meal_list')
    context = get_patient_context(request.user)
    context['foods'] = foods
    return render(request, 'user/meal_add.html', context)

@login_required
def meal_list(request):
    role = getattr(request.user, 'role', '')

    if role == 'patient':
        context = get_patient_context(request.user)
        return render(request, 'user/meal_list.html', context)

    elif role == 'dietitian':
        meals = MealLog.objects.all()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()

        context = {
            'meals': meals,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
            'total_messages': total_messages,
        }
        return render(request, 'user/meal_list.html', context)

    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

@login_required
def meal_edit(request, pk):
    if getattr(request.user, 'role', '') != 'patient':
        return redirect('meal_list')

    meal = get_object_or_404(MealLog, pk=pk, user=request.user)
    foods = Food.objects.all()

    if request.method == 'POST':
        meal.date = request.POST.get('date')
        food_id = request.POST.get('food')
        meal.food = Food.objects.get(id=food_id)
        meal.quantity = request.POST.get('quantity')
        meal.save()
        return redirect('meal_list')

    context = get_patient_context(request.user)
    context.update({'meal': meal, 'foods': foods})
    return render(request, 'user/meal_edit.html', context)

@login_required
def meal_delete(request, pk):
    if getattr(request.user, 'role', '') != 'patient':
        return redirect('meal_list')
    meal = get_object_or_404(MealLog, pk=pk, user=request.user)
    if request.method == "POST":
        meal.delete()
        return redirect('meal_list')

    context = get_patient_context(request.user)
    context['meal'] = meal
    return render(request, 'user/meal_delete.html', context)
