from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .viewsets import SalesFileViewSet
from .models import SalesFile
from unittest.mock import patch  # <-- include at top of file
import tests.mocks


class SalesFileTestCase(TestCase):

    def test_create_salesfile(self):
        request = APIRequestFactory().post('/api-sales/salesfiles/', {
            'filename': 'test.csv',
            'filetype': 'csv',
            'filesize': 100,
        })
        salesfile_create_function = SalesFileViewSet.as_view(
            actions={'post': 'create'})
        response = salesfile_create_function(request)
        print(response.data)   # <-- temporary, we will remove this later
        print("Si llega hasta aqui")
        self.assertEqual(response.status_code, 200)

    # <-- patch the test_request_presigned_url method
    @patch("SalesApp.tasks.boto3", tests.mocks.MockBoto3())
    def test_request_presigned_url(self):
        # organisation = Organisation()
        # organisation.name = "test"
        # organisation.save()

        salesfile = SalesFile(
            filename="test.csv",
            # organisation=organisation,
            filetype="csv",
            filesize=100,
        )
        salesfile.save()
        print(f"El valor del id es: {salesfile.id}")
        request = APIRequestFactory().post(
            f"/api-sales/salesfiles/{salesfile.id}/process/",
            {
                "action": "CREATE_PRESIGNED_URL",
            },
        )
        api_view = SalesFileViewSet.as_view(actions={"post": "process"})
        response = api_view(
            request, pk=salesfile.id
        )
        print("SI LLEGA HASTA ESTE PUNTO")
        print(response.data)
        print("Esto se imprime")
        self.assertEqual(response.data["status"], "ok")
        self.assertIsNotNone(response.data["presigned_url"])
        self.assertEqual(response.data["key"], salesfile.s3_key)
        self.assertEqual(response.status_code, 200)
