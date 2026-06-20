from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from workspace.models import Workspace


from accounts.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
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

@login_required
def dashboard(request):
    leaves = LeaveRequest.objects.all().order_by('-created_at')

    context = {
        'total_leaves': leaves.count(),
        'pending_leaves': leaves.filter(status='PENDING').count(),
        'approved_leaves': leaves.filter(status='APPROVED').count(),
        'rejected_leaves': leaves.filter(status='REJECTED').count(),
        'recent_leaves': leaves[:5],
    }

    return render(request, 'dashboard.html', context)


@csrf_exempt
def login_page(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("my_leaves_page")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})


def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required
def apply_leave_page(request):
    workspaces = Workspace.objects.all()

    if request.method == "POST":
        workspace_id = request.POST.get("workspace")
        reason = request.POST.get("reason")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        workspace = Workspace.objects.get(id=workspace_id)

        LeaveRequest.objects.create(
            user=request.user,
            workspace=workspace,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            status="PENDING"
        )

        return redirect("my_leaves_page")

    return render(request, "apply_leave.html", {"workspaces": workspaces})


@login_required
def my_leaves_page(request):
    leaves = LeaveRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_leaves.html", {"leaves": leaves})



def signup_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                "signup.html",
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "signup.html",
                {"error": "Username already exists"}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login_page")

    return render(request, "signup.html")