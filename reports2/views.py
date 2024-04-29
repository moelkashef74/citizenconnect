# views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Report_cat_two
from .serializers import ReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CreateReportView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
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
            Report = Report_cat_two.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if Report.status != "reported":
            return Response({"error": "Report is not in reported status"}, status=400)

        Report.status = "approved"
        Report.save()

        return Response(status=200)

class RejectReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            Report = Report_cat_two.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if Report.status != "reported":
            return Response({"error": "Report is not in reported status"}, status=400)

        Report.status = "rejected"
        Report.save()

        return Response(status=200)

class SolvedReportView(APIView):
    def post(self, request, Report_id, format=None):
        try:
            Report = Report_cat_two.objects.get(id=Report_id)
        except Report.DoesNotExist:
            return Response(status=404)

        if Report.status != "approved":
            return Response({"error": "Report is not in reported status"}, status=400)

        Report.status = "solved"
        Report.save()

        return Response(status=200)           
    
class SolvedTimelineView(ListAPIView):
    queryset = Report_cat_two.objects.filter(status="solved").order_by('-created_at')
    serializer_class = ReportSerializer


class ReportedTimelineView(ListAPIView):
    queryset = Report_cat_two.objects.filter(status="reported").order_by('-created_at')
    serializer_class = ReportSerializer


class ApprovedTimelineView(ListAPIView):
    queryset = Report_cat_two.objects.filter(status="approved").order_by('-created_at')
    serializer_class = ReportSerializer