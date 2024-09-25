from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:   
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        cached_item = cache.get(pk)
        if cached_item:
            return Response(cached_item, status=status.HTTP_200_OK)

        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item)
            cache.set(pk, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.set(pk, serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            item.delete()
            cache.delete(pk)
            return Response({"detail": "Item deleted successfully."}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
