from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from workspace.models import Membership


class LeaveRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        memberships = Membership.objects.filter(user=user)

        if memberships.filter(role='OWNER').exists():
            return LeaveRequest.objects.all()

        admin_workspaces = memberships.filter(
            role='ADMIN'
        ).values_list('workspace_id', flat=True)

        if admin_workspaces.exists():
            return LeaveRequest.objects.filter(
                workspace_id__in=admin_workspaces
            )

        return LeaveRequest.objects.filter(user=user)


class UpdateLeaveStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        leave = LeaveRequest.objects.get(id=pk)

        membership = Membership.objects.filter(
            user=request.user,
            workspace=leave.workspace
        ).first()

        if not membership or membership.role not in ['ADMIN', 'OWNER']:
            return Response(
                {"error": "You are not allowed to update this leave request"},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')

        if new_status not in ['APPROVED', 'REJECTED']:
            return Response(
                {"error": "Status must be APPROVED or REJECTED"},
                status=status.HTTP_400_BAD_REQUEST
            )

        leave.status = new_status
        leave.approval_comment = request.data.get('comment', '')
        leave.approved_by = request.user
        leave.approved_at = timezone.now()
        leave.save()
        return Response({"message": f"Leave {new_status} successfully"})