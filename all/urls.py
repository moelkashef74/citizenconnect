# central_reports/urls.py
from django.urls import path
from .views import SolvedTimelineView, ReportedTimelineView, ApprovedTimelineView

urlpatterns = [
    path('timeline/solved/', SolvedTimelineView.as_view(), name='solved-timeline'),
    path('timeline/reported/', ReportedTimelineView.as_view(), name='reported-timeline'),
    path('timeline/approved/', ApprovedTimelineView.as_view(), name='approved-timeline'),
    # # Add paths for 'reported' and 'approved' timelines
]
