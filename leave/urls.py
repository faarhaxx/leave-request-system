from django.urls import path
from .views import LeaveRequestListCreateView, UpdateLeaveStatusView
from .views import LeaveRequestListCreateView, UpdateLeaveStatusView, dashboard


urlpatterns = [
    path('', LeaveRequestListCreateView.as_view()),
    path('<int:pk>/status/', UpdateLeaveStatusView.as_view()),
    path('dashboard/', dashboard, name='dashboard'),

]
