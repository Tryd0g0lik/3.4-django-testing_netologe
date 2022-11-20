from django.urls import path, include
from rest_framework.routers import DefaultRouter

from students.views import CoursesViewSet, StudentViewSet

router = DefaultRouter()
router.register("courses/", CoursesViewSet, basename="courses")
router.register('student/', StudentViewSet, basename="student")


urlpatterns = [
	# path(" ", include(router.urls)),
] + router.urls