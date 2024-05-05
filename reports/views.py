# views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Report
from .serializers import ReportSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from accounts.models import User


class CreateReport1View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'cat1'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateReport2View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'cat2'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateReport3View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'cat3'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateReportOtherView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'other'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ApproveReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            report = Report.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if report.status != "reported":
            return Response({"error": "Report is not in reported status"}, status=400)

        report.status = "approved"
        report.save()

        return Response(status=200)

class RejectReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            report = Report.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if report.status != "reported":
            return Response({"error": "Report is not in reported status"}, status=400)

        report.status = "rejected"
        report.save()

        return Response(status=200)

class SolvedReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            report = Report.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if report.status != "approved":
            return Response({"error": "Report is not in approved status"}, status=400)

        report.status = "solved"
        report.save()

        return Response(status=200)

class SolvedTimelineView(ListAPIView):
    queryset = Report.objects.filter(status="solved").order_by('-created_at')
    serializer_class = ReportSerializer


class ReportedTimelineView(ListAPIView):
    queryset = Report.objects.filter(status="reported").order_by('-created_at')
    serializer_class = ReportSerializer


class ApprovedTimelineView(ListAPIView):
    queryset = Report.objects.filter(status="approved").order_by('-created_at')
    serializer_class = ReportSerializer


class Cat1TimelineView(ListAPIView):
    queryset = Report.objects.filter(category="cat1", status="solved").order_by('-created_at')
    serializer_class = ReportSerializer

class Cat2TimelineView(ListAPIView):
    queryset = Report.objects.filter(category="cat2", status="solved" ).order_by('-created_at')
    serializer_class = ReportSerializer

class Cat3TimelineView(ListAPIView):
    queryset = Report.objects.filter(category="cat3", status="solved").order_by('-created_at')
    serializer_class = ReportSerializer

class OtherTimelineView(ListAPIView):
    queryset = Report.objects.filter(status="solved").exclude(category__in=["cat1", "cat2", "cat3"]).order_by('-created_at')
    serializer_class = ReportSerializer


class UserReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filter reports by the current authenticated user
        reports = Report.objects.filter(user=request.user).order_by('-created_at')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
    

class UserDetailView(APIView):
    def get(self, request, email, format=None):
        try:
            user = User.objects.get(email_or_phone=email)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)