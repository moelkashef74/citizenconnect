from django.urls import path
from .views import CreateProblemView, ProblemTimelineView

urlpatterns = [
    path('report/create/', CreateProblemView.as_view(), name='create_problem'),
    path('report/timeline/', ProblemTimelineView.as_view(), name='problem_timeline'),
]