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
from datetime import datetime


class CreateReport1View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'Environmental'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json; charset=utf-8')


        
class CreateReport2View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'Road'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json; charset=utf-8')
        
class CreateReport3View(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        # Set a default category here
        default_category = 'Electric'  # Replace with your desired default category
        request.data['category'] = default_category  # Set the default category in the request data

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the report to the current user before saving
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json; charset=utf-8')
        
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
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json; charset=utf-8')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json; charset=utf-8')
        


class ApproveReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            report = Report.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if report.status != "reported":
            return Response({"error": "Report is not in reported status"}, status=400)

        report.status = "approved"
        if report.notification is None:
            report.notification = []
        report.notification.append({
    'message': f"Report {report.id} has been approved.",
    'timestamp': datetime.now().isoformat(),
    'id': report.id
})
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
        if report.notification is None:
            report.notification = []
        report.notification.append({
    'message': f"Report {report.id} has been rejected.",
    'timestamp': datetime.now().isoformat(),
    'id': report.id
        })
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
        if report.notification is None:
            report.notification = []
        report.notification.append({
    'message': f"Report {report.id} has been solved.",
    'timestamp': datetime.now().isoformat(),
    'id': report.id
        })
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
    queryset = Report.objects.filter(category="Environmental", status="solved").order_by('-created_at')
    serializer_class = ReportSerializer

class Cat2TimelineView(ListAPIView):
    queryset = Report.objects.filter(category="Road", status="solved" ).order_by('-created_at')
    serializer_class = ReportSerializer

class Cat3TimelineView(ListAPIView):
    queryset = Report.objects.filter(category="Electric", status="solved").order_by('-created_at')
    serializer_class = ReportSerializer

class OtherTimelineView(ListAPIView):
    queryset = Report.objects.filter(category="other", status="solved").order_by('-created_at')
    serializer_class = ReportSerializer


class UserReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filter reports by the current authenticated user
        reports = Report.objects.filter(user=request.user).order_by('-created_at')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
    

class UserDetailView(APIView):
    def get(self, request, phone, format=None):
        try:
            user = User.objects.get(phone=phone)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filter reports by the current authenticated user and exclude reports without a notification
        reports = Report.objects.filter(user=request.user).exclude(notification__isnull=True).order_by('-created_at')

        # Concatenate all notifications into a single list
        notifications = [note for report in reports for note in report.notification]

        # Sort notifications by timestamp
        notifications.sort(key=lambda x: x['timestamp'], reverse=True)

        return Response(notifications)

class LastSolvedReportView(APIView):
    def get(self, request, *args, **kwargs):
        categories = dict(Report.CATEGORY_CHOICES).keys()  # Use the database values
        data = []
        for category in categories:
            last_solved_report = Report.objects.filter(category=category, status='solved').first()
            if last_solved_report:
                serializer = ReportSerializer(last_solved_report)
                data.append(serializer.data)
        return Response(data)