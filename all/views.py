# central_reports/views.py
from rest_framework.generics import ListAPIView
from reports.models import Report 
from reports2.models import Report_cat_two 
from reports3.models import Report_cat_three
from other_cat.models import Report_other
from reports.serializers import ReportSerializer


class SolvedTimelineView(ListAPIView):
    serializer_class = ReportSerializer
    def get_queryset(self):
        report = Report.objects.filter(status="solved")
        report2 = Report_cat_two.objects.filter(status="solved")
        report3 = Report_cat_three.objects.filter(status="solved")
        other =  Report_other.objects.filter(status="solved")  
        
        return report.union(report2, report3, other).order_by('-created_at')


class ReportedTimelineView(ListAPIView):
    serializer_class = ReportSerializer
    def get_queryset(self):
        report = Report.objects.filter(status="reported")
        report2 = Report_cat_two.objects.filter(status="reported")
        report3 = Report_cat_three.objects.filter(status="reported")
        other =  Report_other.objects.filter(status="reported")     
        return report.union(report2, report3, other).order_by('-created_at')


class ApprovedTimelineView(ListAPIView):
    serializer_class = ReportSerializer
    def get_queryset(self):
        report = Report.objects.filter(status="approved")
        report2 = Report_cat_two.objects.filter(status="approved")
        report3 = Report_cat_three.objects.filter(status="approved")
        other =  Report_other.objects.filter(status="approved")  
        
        return report.union(report2, report3, other).order_by('-created_at')