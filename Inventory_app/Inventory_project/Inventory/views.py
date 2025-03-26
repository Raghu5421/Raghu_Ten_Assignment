from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inventory, Member, Booking, MAX_BOOKINGS
from .serializers import InventorySerializer, MemberSerializer, BookingSerializer
import pandas as pd
    
# Inventory ViewSet
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


# Member ViewSet
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


# Booking ViewSet
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Home Endpoint
@api_view(['GET'])
def home(request):
    """API Home Page"""
    return Response({
        "message": "Welcome to the Inventory Management API!",
        "endpoints": {
            "upload_inventory": "/upload-inventory/",
            "upload_members": "/upload-members/",
            "inventory": "/api/inventory/",
            "members": "/api/members/",
            "bookings": "/api/bookings/",
            "cancel_booking": "/api/bookings/<booking_id>/"
        }
    })

@api_view(['POST'])
def book(request):
    """Book an item from the inventory for a member"""
    member_id = request.data.get('member_id')
    inventory_id = request.data.get('inventory_id')

    try:
        member = Member.objects.get(id=member_id)
        inventory = Inventory.objects.get(id=inventory_id)

        if member.booking_count >= MAX_BOOKINGS:
            return Response({'error': 'Member has reached the maximum booking limit'}, status=400)

        if inventory.remaining_count <= 0:
            return Response({'error': 'No items left in inventory'}, status=400)

        with transaction.atomic():
            # Create booking record
            booking = Booking.objects.create(
                member=member,
                inventory=inventory,
                booking_date=timezone.now()
            )

            # Update booking count and inventory count
            member.booking_count += 1
            inventory.remaining_count -= 1
            member.save()
            inventory.save()

        return Response({
            'message': 'Booking successful',
            'booking_reference': str(booking.reference)
        }, status=201)

    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=404)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory item not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def cancel_booking(request):
    """Cancel a booking by reference"""
    reference = request.data.get('reference')

    try:
        booking = Booking.objects.get(reference=reference)
        member = booking.member
        inventory = booking.inventory

        with transaction.atomic():
            # Delete the booking
            booking.delete()

            # Update booking count and inventory count
            member.booking_count -= 1
            inventory.remaining_count += 1
            member.save()
            inventory.save()

        return Response({'message': 'Booking cancelled successfully'}, status=200)

    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# CSV Upload Endpoints
@api_view(['POST'])
def upload_inventory(request):
    """Upload inventory from CSV"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File is not in CSV format'}, status=400)

    try:
        df = pd.read_csv(csv_file)

        # Validate required columns
        required_columns = {'title', 'description', 'remaining_count', 'expiration_date'}
        if not required_columns.issubset(df.columns):
            return Response({'error': 'Missing required columns'}, status=400)

        # Convert expiration_date to datetime
        df['expiration_date'] = pd.to_datetime(df['expiration_date'], errors='coerce').dt.date
        df = df.dropna()

        with transaction.atomic():
            for _, row in df.iterrows():
                Inventory.objects.create(
                    title=row['title'],
                    description=row['description'],
                    remaining_count=row['remaining_count'],
                    expiration_date=row['expiration_date']
                )

        return Response({'message': 'Inventory uploaded successfully'}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def upload_members(request):
    """Upload members from CSV"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File is not in CSV format'}, status=400)

    try:
        df = pd.read_csv(csv_file)

        # Validate required columns
        required_columns = {'name', 'surname', 'booking_count', 'date_joined'}
        if not required_columns.issubset(df.columns):
            return Response({'error': 'Missing required columns'}, status=400)

        # Convert date_joined to datetime
        df['date_joined'] = pd.to_datetime(df['date_joined'], errors='coerce')
        df = df.dropna()

        with transaction.atomic():
            for _, row in df.iterrows():
                Member.objects.create(
                    name=row['name'],
                    surname=row['surname'],
                    booking_count=row['booking_count'],
                    date_joined=row['date_joined']
                )

        return Response({'message': 'Members uploaded successfully'}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
