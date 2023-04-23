from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='post')
router_v1.register(r'groups', GroupViewSet, basename='group')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(
        'v1/redoc/',
        TemplateView.as_view(template_name='api/redoc.html'),
        name='redoc'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
