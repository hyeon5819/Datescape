from rest_framework.response import Response
from rest_framework.views import APIView
from notification.models import Notification
from rest_framework import status, permissions


class NotificationView(APIView):
    def get(self, request):
        if Notification.objects.filter(target_user=request.user, db_status=1):
            return Response({"unread": True}, status=status.HTTP_200_OK)
        else:
            return Response({"unread": False}, status=status.HTTP_200_OK)
