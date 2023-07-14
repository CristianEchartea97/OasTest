from django.urls import path,include
from rest_framework import routers
from . import views 

router = routers.DefaultRouter()
router.register(r'programmers',views.ProgrammerViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls'))  # <----------- add this line to whatever is already there
]