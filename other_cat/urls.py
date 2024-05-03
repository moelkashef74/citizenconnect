from django.urls import path
from .views import ApproveReportView, CreateReportView, SolvedTimelineView, RejectReportView, SolvedReportView,  ReportedTimelineView, ApprovedTimelineView

urlpatterns = [
    path('report/create/', CreateReportView.as_view(), name='create_Report'),
    path('report/solved/timeline/', SolvedTimelineView.as_view(), name='solved_timeline'),
    path('report/reported/timeline/', ReportedTimelineView.as_view(), name='reported_timeline'),
    path('report/approved/timeline/', ApprovedTimelineView.as_view(), name='approved_timeline'),
    path('report/<str:Report_id>/approve/', ApproveReportView.as_view(), name='approve-Report'),
    path('report/<str:Report_id>/reject/', RejectReportView.as_view(), name='reject-Report'),
    path('report/<str:Report_id>/solved/', SolvedReportView.as_view(), name='solved-Report'),
]