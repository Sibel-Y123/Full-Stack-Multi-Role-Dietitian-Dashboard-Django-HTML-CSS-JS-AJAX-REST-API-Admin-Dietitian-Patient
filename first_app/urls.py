from django.urls import path
from . import views
from .views import food_views
from .views import fetch_customers_view, user_stats
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm
from django.urls import reverse_lazy



urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    path('mylogin/', views.my_login_view, name='mylogin'),
    path('logout/',  views.my_logout_view,name='logout'),
    path('dietitian/dashboard/', views.dietitian_dashboard, name='dietitian_dashboard'),



    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),


    path('customers/', views.customer_list, name='customer_list'),
    path('customers/edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('customers/add/', views.customer_add, name='customer_add'), 
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),


    path('diet-plans/', views.diet_plan_list, name='diet_plan_list'),
    path('diet-plans/add/', views.diet_plan_add, name='diet_plan_add'),
    path('diet-plans/edit/<int:pk>/', views.diet_plan_edit, name='diet_plan_edit'),
    path('diet-plans/delete/<int:pk>/', views.diet_plan_delete, name='diet_plan_delete'),


    path('foods/', views.food_list, name='food_list'),
    path('foods/import/', views.import_foods_from_usda, name='food_import'),
   
    
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/add/', views.meal_add, name='meal_add'),
    path('meals/edit/<int:pk>/', views.meal_edit, name='meal_edit'),
    path('meals/delete/<int:pk>/', views.meal_delete, name='meal_delete'),

   
    path('messages/', views.message_list, name='message_list'),
    path('messages/send/', views.message_send, name='message_send'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/delete/<int:pk>/', views.message_delete, name='message_delete'),
    path('messages/edit/<int:pk>/', views.message_edit, name='message_edit'),



 
    path("fetch-customers/", views.fetch_customers_view, name="fetch_customers"),

    path("patient-registrations-trend/", views. patient_registrations_trend , name="patient_registrations_trend"),
    path("patient-activity-trend/", views.patient_activity_trend, name="patient_activity_trend"),
    path('bmi-by-gender/', views.bmi_by_gender, name='bmi_by_gender'),
    path('bmi-by-age/', views.bmi_by_age, name='bmi_by_age'),
    path('total-messages-trend/', views.total_messages_trend, name='total_messages_trend'),
    path('total-dietplans-trend/', views.total_dietplans_trend, name='total_dietplans_trend'),
    path('dietitian/dashboard/', views.dietitian_dashboard, name='dietitian_dashboard'),

   
    path('api/user-stats/', views.user_stats, name='user_stats'),


   
   
   
   path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

  
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='patient/password_change.html',form_class=CustomPasswordChangeForm,success_url='/password_change/done/' ),
    name='password_change'
     ),

    path(
    'password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='patient/password_change_done.html'),
    name='password_change_done'
     ),

    
    
  


    
]




