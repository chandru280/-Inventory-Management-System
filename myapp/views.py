from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Item
from .serializers import ItemSerializer, RegisterSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                "data": serializer.data,
                "success": True,
                "status": 200,
                "message": "Item Created Successfully"
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                "status": 400,
                "message": serializer.errors
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

    
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        content_data = {
            "data": serializer.data,
            "success": True,
            "status": 200,
            "message": "Items Found"
        }
        return Response(content_data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        cached_item = cache.get(pk)
        if cached_item:
            return Response(cached_item, status=status.HTTP_200_OK)

        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item)
            cache.set(pk, serializer.data)
            content_data = {
                "data": serializer.data,
                "success": True,
                "status": 200,
                "message": "Item Found"
            }
            return Response(content_data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            content_data = {
                "status": 400,
                "message": "Item not found."
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.set(pk, serializer.data)   
                content_data = {
                    "data": serializer.data,
                    "success": True,
                    "status": 200,
                    "message": "Item Updated Successfully"
                }
                return Response(content_data, status=status.HTTP_200_OK)
            else:
                content_data = {
                    "status": 400,
                    "message": serializer.errors
                }
                return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            content_data = {
                "status": 400,
                "message": "Item not found."
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            item.delete()
            cache.delete(pk)   
            content_data = {
                "success": True,
                "status": 200,
                "message": "Item Deleted Successfully"
            }
            return Response(content_data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            content_data = {
                "status": 400,
                "message": "Item not found."
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

 