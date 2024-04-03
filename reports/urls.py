from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.ProblemListCreateAPIView.as_view(), name='problem-create'),
]