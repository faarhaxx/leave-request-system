from rest_framework import generics
from .models import Workspace, Membership
from .serializers import WorkspaceSerializer, MembershipSerializer


class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

# Create your views here.
