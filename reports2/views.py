# views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Problem_cat_two
from .serializers import ProblemSerializer

class CreateProblemView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class ProblemTimelineView(ListAPIView):
    queryset = Problem_cat_two.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer