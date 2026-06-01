from django.urls import path
from .views import LeaveRequestListCreateView, UpdateLeaveStatusView

urlpatterns = [
    path('', LeaveRequestListCreateView.as_view()),
    path('<int:pk>/status/', UpdateLeaveStatusView.as_view()),
]




