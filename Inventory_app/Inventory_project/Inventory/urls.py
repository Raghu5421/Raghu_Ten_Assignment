from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MemberViewSet, BookingViewSet, book, cancel_booking, upload_inventory, upload_members, home

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'members', MemberViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('upload-inventory/', upload_inventory, name='upload_inventory'),
    path('upload-members/', upload_members, name='upload_members'),
    path('book/', book, name='book'),
    path('cancel/', cancel_booking, name='cancel_booking'),
    path('api/', include(router.urls)),
]
