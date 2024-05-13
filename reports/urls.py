from django.urls import path
from .views import ApproveReportView, CreateReport1View, CreateReport2View, CreateReport3View, CreateReportOtherView, SolvedTimelineView, RejectReportView, SolvedReportView,  ReportedTimelineView, ApprovedTimelineView, Cat1TimelineView,Cat2TimelineView,Cat3TimelineView, OtherTimelineView, UserReportsView, UserDetailView

urlpatterns = [
    path('env/create/', CreateReport1View.as_view(), name='create_env_Report'),
    path('traffic/create/', CreateReport2View.as_view(), name='create_traffic_Report'),
    path('electric/create/', CreateReport3View.as_view(), name='create_electric_Report'),
    path('other/create/', CreateReportOtherView.as_view(), name='create_Report_other'),
    path('solved/timeline/', SolvedTimelineView.as_view(), name='solved_timeline'),
    path('reported/timeline/', ReportedTimelineView.as_view(), name='reported_timeline'),
    path('approved/timeline/', ApprovedTimelineView.as_view(), name='approved_timeline'),
    path('<str:Report_id>/approve/', ApproveReportView.as_view(), name='approve-Report'),
    path('<str:Report_id>/reject/', RejectReportView.as_view(), name='reject-Report'),
    path('<str:Report_id>/solved/', SolvedReportView.as_view(), name='solved-Report'),
    path('env/timeline/', Cat1TimelineView.as_view(), name='env-timeline'),
    path('traffic/timeline/', Cat2TimelineView.as_view(), name='traffic-timeline'),
    path('electric/timeline/', Cat3TimelineView.as_view(), name='electric-timeline'),
    path('other/timeline/', OtherTimelineView.as_view(), name='other-timeline'),
    path('user-reports/', UserReportsView.as_view(), name='user-reports'),
    path('user-detail/<str:email>/', UserDetailView.as_view(), name='user-detail-by-email'),
]