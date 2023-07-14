from rest_framework import routers
from .viewsets import SalesFileViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register(r'salesfiles', SalesFileViewSet)

#urlpatterns = router.urls

urlpatterns = [
	path('', include(router.urls)),
	path('api-sales/', include('rest_framework.urls'))  # <----------- add this line to whatever is already there
]