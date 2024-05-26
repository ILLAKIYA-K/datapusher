from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer = DestinationSerializer

class IncomingDataView(APIView):
    def post(self, request):
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        account = get_object_or_404(Account, app_secret_token=app_secret_token)
        data = request.data

        for destination in account.destinations.all():
            headers = destination.headers
            method = destination.http_method.upper()
            url = destination.url

            if method == 'GET':
                response = requests.get(url, params=data, headers=headers)
            else:
                response = requests.request(method, url, json=data, headers=headers)
        
        return Response({"message": "Data processed"}, status=status.HTTP_200_OK)
