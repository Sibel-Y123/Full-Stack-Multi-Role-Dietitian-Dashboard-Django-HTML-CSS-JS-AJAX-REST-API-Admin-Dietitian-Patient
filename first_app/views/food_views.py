from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Food, CustomerData, User, DietPlan, Message
import requests
from django.conf import settings
from django.http import JsonResponse




@login_required
def food_list(request):
    
    if request.user.role != 'dietitian':
        return redirect('dashboard')

    foods = Food.objects.all()

 
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
        'foods': foods,
        'total_patients': total_patients,
        'total_diet_plans': total_diet_plans,
        'avg_bmi': avg_bmi,
        'total_messages': total_messages,
        'customers': customers,
    }

    return render(request, 'admin/food_list.html', context)


@login_required
def import_foods_from_usda(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({'success': False, 'foods': []})

    api_key = settings.USDA_API_KEY
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}"

   
    payload = {
        "query": query,
        "dataType": ["Foundation", "SR Legacy"],
        "pageSize": 5
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

    data = response.json()
    foods_data = data.get("foods", [])

    results = []
    for item in foods_data:
        
        name = item.get("description", "Unknown")
        nutrients = {n["nutrientName"]: n["value"] for n in item.get("foodNutrients", [])}

        food_obj, _ = Food.objects.update_or_create(
            name=name,
            defaults={
                "calories": nutrients.get("Energy", 0),
                "protein": nutrients.get("Protein", 0),
                "carbs": nutrients.get("Carbohydrate, by difference", 0),
                "fat": nutrients.get("Total lipid (fat)", 0),
                "vitamin_c": nutrients.get("Vitamin C, total ascorbic acid", None),
                "iron": nutrients.get("Iron, Fe", None),
                "water": nutrients.get("Water", None),
            }
        )

        results.append({
            "id": food_obj.id,
            "name": food_obj.name,
            "calories": food_obj.calories,
            "protein": food_obj.protein,
            "carbs": food_obj.carbs,
            "fat": food_obj.fat,
            "vitamin c": food_obj.vitamin_c,
            "iron": food_obj.iron,
            "water": food_obj.water,
        })

    return JsonResponse({'success': True, 'foods': results})

