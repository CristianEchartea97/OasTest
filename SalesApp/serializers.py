from rest_framework import serializers
from .models import SalesFile


class SalesFileSerializer(serializers.ModelSerializer):
    class Meta:            # <--what is this? see note below
        model = SalesFile
        fields = '__all__'


class SalesFileActions:
    # This is just a fancy ENUM to list the available actions
    # currently there is only one choice: CREATE_PRESIGNED_URL
    # in the future we can implement CREATE_DOWNLOAD_URL, or
    # REIMPORT_SALESFILE, etc.
    CREATE_PRESIGNED_URL = "CREATE_PRESIGNED_URL"
    START_SALESFILE_IMPORT = "START_SALESFILE_IMPORT"
    CHOICES = [
        (CREATE_PRESIGNED_URL, "create presigned url"),
        (START_SALESFILE_IMPORT, "start salesfile import"),
    ]


class SalesFileProcessSerializer(serializers.Serializer):
    # A Serializer that defines the format of the salesfile process
    # request and validates the data. It has just one field, `action`
    # which can be a value from the SalesFileActions.CHOICES list,
    # defined above.
    action = serializers.ChoiceField(
        choices=SalesFileActions.CHOICES,
    )


class SalesFileProcessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    presigned_url = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
