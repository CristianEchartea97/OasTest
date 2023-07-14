from rest_framework import viewsets
from .models import SalesFile
from .serializers import SalesFileSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import SalesFileProcessSerializer
from .serializers import SalesFileActions
from .serializers import SalesFileProcessResponseSerializer


class SalesFileViewSet(viewsets.ModelViewSet):
    queryset = SalesFile.objects.all()
    serializer_class = SalesFileSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        sales_file = self.get_object()
        serializer = SalesFileProcessSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            action = serializer.validated_data["action"]
            if action == SalesFileActions.CREATE_PRESIGNED_URL:
                presigned_url = sales_file.generate_presigned_url()
                response = SalesFileProcessResponseSerializer(
                    {
                        "status": "ok",
                        "presigned_url": presigned_url,
                        "key": sales_file.s3_key,
                    }
                )
            return Response(response.data)
        return Response({"status": "error"})
