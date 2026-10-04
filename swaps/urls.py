from django.urls import path
from .views import CreateSwapRequestView, UpdateSwapRequestStatusView

urlpatterns = [
    path('create/<int:listing_id>/', CreateSwapRequestView.as_view(), name='swap_create'),
    path('<int:pk>/<str:action>/', UpdateSwapRequestStatusView.as_view(), name='swap_status_update'),
]
