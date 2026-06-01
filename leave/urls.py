from django.urls import path
from .views import (
    LeaveRequestListCreateView,
    UpdateLeaveStatusView,
    dashboard,
    login_page,
    logout_page,
    apply_leave_page,
    my_leaves_page,
)

urlpatterns = [
    path('', LeaveRequestListCreateView.as_view()),
    path('<int:pk>/status/', UpdateLeaveStatusView.as_view()),
    path('dashboard/', dashboard, name='dashboard'),

    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('apply/', apply_leave_page, name='apply_leave_page'),
    path('my-leaves/', my_leaves_page, name='my_leaves_page'),
]
