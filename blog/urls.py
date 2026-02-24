# from django.urls import path
# from . import views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('blogs/', views.blog_list),
#     path('blogs/<int:pk>/', views.blog_detail),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]


from rest_framework.routers import DefaultRouter
from .views import BlogViewSet,CommentViewSet,FollowViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'comments', CommentViewSet)
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = router.urls