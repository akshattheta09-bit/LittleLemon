from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Reservation

def home(request):
    return render(request, 'Lemons/home.html')

def about(request):
    return render(request, 'Lemons/about.html')

def menu(request):
    return render(request, 'Lemons/menu.html')

def reservation_page(request):
    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name')
        reservation_date = request.POST.get('reservation_date')
        reservation_slot = request.POST.get('reservation_slot')

        # Check for duplicate booking
        if Reservation.objects.filter(reservation_date=reservation_date, reservation_slot=reservation_slot).exists():
            return render(request, 'Lemons/reservation.html', {
                'error': 'This time slot is already booked for the selected date.',
                'first_name': first_name,
                'reservation_date': reservation_date,
                'reservation_slot': reservation_slot,
            })

        # Create the reservation
        reservation = Reservation.objects.create(
            first_name=first_name,
            reservation_date=reservation_date,
            reservation_slot=reservation_slot
        )

        # After successful booking, show success message with JSON data
        reservation_data = {
            'id': reservation.id,
            'first_name': reservation.first_name,
            'reservation_date': str(reservation.reservation_date),
            'reservation_slot': reservation.reservation_slot
        }
        
        return render(request, 'Lemons/reservation.html', {
            'success': 'Reservation made successfully!',
            'reservation_data': reservation_data,
            'reservation_json': json.dumps(reservation_data, indent=2),
            'first_name': '',
            'reservation_date': timezone.now().date(),
            'reservation_slot': '',
        })

    # GET request: show the form
    # Get the selected date from query parameters, default to today
    selected_date = request.GET.get('date', timezone.now().date())
    # Get all reservations for the selected date
    reservations = Reservation.objects.filter(reservation_date=selected_date).order_by('reservation_slot')

    context = {
        'reservations': reservations,
        'selected_date': selected_date,
        'first_name': '',
        'reservation_date': selected_date,
        'reservation_slot': '',
    }
    return render(request, 'Lemons/reservation.html', context)

@csrf_exempt
def reservation_api(request):
    if request.method == 'GET':
        # Get the date from query parameters, if provided
        date_param = request.GET.get('date')
        if date_param:
            reservations = Reservation.objects.filter(reservation_date=date_param)
        else:
            reservations = Reservation.objects.all()

        # Convert to list of dictionaries
        data = list(reservations.values('first_name', 'reservation_date', 'reservation_slot'))
        return JsonResponse(data, safe=False)

    # We don't handle other methods for now
    return JsonResponse({'error': 'Method not allowed'}, status=405)
