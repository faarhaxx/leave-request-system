from django.urls import path
from .views import WorkspaceListCreateView, MembershipListCreateView

urlpatterns = [
    path('', WorkspaceListCreateView.as_view()),
    path('members/', MembershipListCreateView.as_view()),
]