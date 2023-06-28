from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from knox.views import LoginView, LogoutView, LogoutAllView
from .views import *

app_name = "api"

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet)
router.register(r"topics", views.TopicViewSet)
router.register(r"subjects", views.SubjectViewSet)
router.register(r"users", views.UsersViewSet)
router.register(r"groups", views.GroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api-key", views.generateAPIKey, name="generate-api-key"),
    path(
        "api-key/expire/<str:digest>",
        views.expireAPIKey,
        name="expire-api-key",
    ),
    path("v1/", include(router.urls)),
    re_path(r"v1/auth/get-token", LoginView.as_view(), name="knox_login"),
    re_path(r"v1/auth/delete-token", LogoutView.as_view(), name="knox_logout"),
    re_path(
        r"v1/auth/delete-all-tokens",
        LogoutAllView.as_view(),
        name="knox_logoutall",
    ),
    # path('v1/login', LoginView.as_view()),
    # path('v1/logout',LogoutView.as_view()),
    # path('v1/logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
