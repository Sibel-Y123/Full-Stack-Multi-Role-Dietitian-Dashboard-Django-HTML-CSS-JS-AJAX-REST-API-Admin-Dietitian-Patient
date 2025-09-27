from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import RiskAnalysis

@login_required
def risk_list(request):
    if request.user.role not in ['dietitian', 'admin']:
        return redirect('dashboard')
    risks = RiskAnalysis.objects.all()
    return render(request, 'dietitian/risk_list.html', {'risks': risks})

@login_required
def risk_add(request):
    if request.user.role != 'dietitian':
        return redirect('dashboard')
    if request.method == 'POST':
        RiskAnalysis.objects.create(
            user_id=request.POST['user'],
            bmi=request.POST['bmi'],
            risk_level=request.POST['risk_level'],
            notes=request.POST.get('notes', '')
        )
        return redirect('risk_list')
    return render(request, 'dietitian/risk_add.html')

@login_required
def risk_edit(request, pk):
    if request.user.role != 'dietitian':
        return redirect('dashboard')
    risk = get_object_or_404(RiskAnalysis, pk=pk)
    if request.method == 'POST':
        risk.bmi = request.POST['bmi']
        risk.risk_level = request.POST['risk_level']
        risk.notes = request.POST.get('notes', '')
        risk.save()
        return redirect('risk_list')
    return render(request, 'dietitian/risk_edit.html', {'risk': risk})

@login_required
def risk_delete(request, pk):
    if request.user.role != 'dietitian':
        return redirect('dashboard')
    risk = get_object_or_404(RiskAnalysis, pk=pk)
    risk.delete()
    return redirect('risk_list')
