from django.urls import path
from .views import ApproveReportView, CreateReport1View, CreateReport2View, CreateReport3View, CreateReportOtherView, SolvedTimelineView, RejectReportView, SolvedReportView,  ReportedTimelineView, ApprovedTimelineView, Cat1TimelineView,Cat2TimelineView,Cat3TimelineView, OtherTimelineView

urlpatterns = [
    path('cat1/create/', CreateReport1View.as_view(), name='create_Report1'),
    path('cat2/create/', CreateReport2View.as_view(), name='create_Report2'),
    path('cat3/create/', CreateReport3View.as_view(), name='create_Report3'),
    path('other/create/', CreateReportOtherView.as_view(), name='create_Report_other'),
    path('solved/timeline/', SolvedTimelineView.as_view(), name='solved_timeline'),
    path('reported/timeline/', ReportedTimelineView.as_view(), name='reported_timeline'),
    path('approved/timeline/', ApprovedTimelineView.as_view(), name='approved_timeline'),
    path('<str:Report_id>/approve/', ApproveReportView.as_view(), name='approve-Report'),
    path('<str:Report_id>/reject/', RejectReportView.as_view(), name='reject-Report'),
    path('<str:Report_id>/solved/', SolvedReportView.as_view(), name='solved-Report'),
    path('cat1/timeline/', Cat1TimelineView.as_view(), name='cat1-timeline'),
    path('cat2/timeline/', Cat2TimelineView.as_view(), name='cat2-timeline'),
    path('cat3/timeline/', Cat3TimelineView.as_view(), name='cat3-timeline'),
    path('other/timeline/', OtherTimelineView.as_view(), name='other-timeline'),
]