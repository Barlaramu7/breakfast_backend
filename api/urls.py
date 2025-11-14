from django.urls import path 
from . import views 

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/', views.login, name='login'),
     path('bookings/', views.create_booking, name='create_booking'),
    path('bookings/<int:user_id>/', views.get_user_bookings, name='get_user_bookings'),
    path('bookings/<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('reset-password/', views.reset_password, name='reset-password'),

]
