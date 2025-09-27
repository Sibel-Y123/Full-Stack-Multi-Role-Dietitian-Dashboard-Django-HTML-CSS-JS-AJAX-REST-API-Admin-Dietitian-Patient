from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from ..models import Message, MealLog, DietPlan, CustomerData

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
def message_list(request):
    role = getattr(request.user, 'role', '')

    if role == 'patient':
        context = get_patient_context(request.user)
        return render(request, 'user/message_list.html', context)
       

    elif role == 'dietitian':
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0

        context = {
            'messages': inbox_messages,
            'sent': sent_messages,
            'total_messages': total_messages,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
        }
        return render(request, 'user/message_list.html', context)

    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)




@login_required
def message_send(request):
    role = getattr(request.user, 'role', '')
    users = User.objects.exclude(id=request.user.id).exclude(role='admin')

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        body = request.POST.get('body')
        recipient = get_object_or_404(User, id=recipient_id)
        Message.objects.create(sender=request.user, receiver=recipient, content=body)
        return redirect('message_list')

    if role == 'patient':
        context = get_patient_context(request.user)
        context['users'] = users
    elif role == 'dietitian':
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0

        context = {
            'users': users,
            'messages': inbox_messages,
            'sent': sent_messages,
            'total_messages': total_messages,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
        }
    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    return render(request, 'user/message_send.html', context)


@login_required
def message_detail(request, pk):
    role = getattr(request.user, 'role', '')
    message = get_object_or_404(Message, pk=pk)

 
    if role == 'patient' and message.receiver != request.user:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    if role == 'patient':
        context = get_patient_context(request.user)
        context['message'] = message
    elif role == 'dietitian':
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0

        context = {
            'message': message,
            'messages': inbox_messages,
            'sent': sent_messages,
            'total_messages': total_messages,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
        }
    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    return render(request, 'user/message_detail.html', context)


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user != message.sender and request.user != message.receiver:
        return redirect('message_list')

    role = getattr(request.user, 'role', '')

    if role == 'patient':
        context = get_patient_context(request.user)
        context['message'] = message
    elif role == 'dietitian':
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0

        context = {
            'message': message,
            'messages': inbox_messages,
            'sent': sent_messages,
            'total_messages': total_messages,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
        }
    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    if request.method == "POST":
        message.delete()
        return redirect('message_list')

    return render(request, 'user/message_delete.html', context)

@login_required
def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user)

    role = getattr(request.user, 'role', '')

    if role == 'patient':
        context = get_patient_context(request.user)
        context['message'] = message
    elif role == 'dietitian':
        inbox_messages = Message.objects.filter(receiver=request.user)
        sent_messages = Message.objects.filter(sender=request.user)
        total_messages = inbox_messages.count() + sent_messages.count()
        total_patients = User.objects.filter(role='patient').count()
        total_diet_plans = DietPlan.objects.count()
        customers = CustomerData.objects.exclude(weight_kg__isnull=True, height_cm__isnull=True)
        total_bmi = sum(c.bmi() for c in customers if c.bmi() is not None)
        avg_bmi = round(total_bmi / len(customers), 2) if customers else 0

        context = {
            'message': message,
            'messages': inbox_messages,
            'sent': sent_messages,
            'total_messages': total_messages,
            'total_patients': total_patients,
            'total_diet_plans': total_diet_plans,
            'avg_bmi': avg_bmi,
        }
    else:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            message.content = body
            message.save()
            return redirect('message_list')

    return render(request, 'user/message_edit.html', context)

