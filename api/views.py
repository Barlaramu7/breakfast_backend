from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Booking
from .serializers import UserSerializer, BookingSerializer
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password


@api_view(['POST'])
def signup(request):
    data = request.data.copy() 
    data['password'] = make_password(data['password'])  #  Hash the password before saving

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password): #  Compare the entered password with the hashed password
            return Response({
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # total_price will auto-calculate
        return Response({"message": "Booking created successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_bookings(request, user_id):
    """
        Automatically delete expired bookings before returning user's active bookings.
        Bookings from today will NOT be deleted — only those before today.
    """
    now = datetime.now().date()  # only compare by date

    expired_bookings = Booking.objects.filter(user_id=user_id, date__lt=now) #  Delete only bookings before today
    expired_count = expired_bookings.count()
    expired_bookings.delete()

    bookings = Booking.objects.filter(user_id=user_id, date__gte=now) #  Keep today's and future bookings
    serializer = BookingSerializer(bookings, many=True)

    return Response({
        "message": f"🧹 Deleted {expired_count} expired bookings",
        "bookings": serializer.data
    })


@api_view(['DELETE'])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return Response({"message": "Booking deleted successfully!"}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"message": "Booking not found!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # total_price auto-updates if guests or price changed
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({"message": "Booking not found!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reset_password(request):
    full_name = request.data.get('full_name')
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(full_name=full_name, email=email)
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "No user found with provided name and email."}, status=status.HTTP_404_NOT_FOUND)

