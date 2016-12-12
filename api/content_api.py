from content.models import Output
from .serializers import OutputSerializer
from rest_framework import viewsets

"""
Contains class based views for REST API endpoints
"""


class OutputViewset(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer
