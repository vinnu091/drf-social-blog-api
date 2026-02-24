# from django.shortcuts import render # Create your views here.
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework.response import Response
# from .models import Blog
# from django.db.models import Q
# from .serializers import BlogSerializer
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from .permissions import IsAuthorOrReadOnly


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from .models import Blog,Comment,Follow
from .serializers import BlogSerializer,CommentSerializer
from .permissions import IsAuthorOrReadOnly

from rest_framework.filters import OrderingFilter
from django.db.models.functions import Lower

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'title_lower']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Blog.objects.select_related('author').all()
        search_query = self.request.query_params.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        return queryset.annotate(title_lower=Lower('title'))
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        blog = self.get_object()
        user = request.user

        if user in blog.likes.all():
            blog.likes.remove(user)
            return Response({'message': 'Unliked'})
        else:
            blog.likes.add(user)
            return Response({'message': 'Liked'})

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('author', 'blog').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_to_follow_id = request.data.get('user_id')

        try:
            user_to_follow = User.objects.get(id=user_to_follow_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()
            return Response({'message': 'Unfollowed'})

        return Response({'message': 'Followed'})

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def blog_list(request):
#     if request.method == 'GET':
#         blogs = Blog.objects.all()

#         search_query = request.GET.get('search')

#         if search_query:
#             blogs = blogs.filter(
#                 Q(title__icontains=search_query) |
#                 Q(content__icontains=search_query)
#             )
#         paginator = PageNumberPagination()
#         # paginator.page_size = 3
#         result_page = paginator.paginate_queryset(blogs, request)
#         serializer = BlogSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#     if request.method == 'POST':
#         serializer = BlogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated, IsAuthorOrReadOnly])
# def blog_detail(request, pk):
#     try:
#         blog = Blog.objects.get(pk=pk)
#     except Blog.DoesNotExist:
#         return Response({"error": "Blog not found"})

#     if request.method == 'GET':
#         serializer = BlogSerializer(blog)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = BlogSerializer(blog, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     if request.method == 'DELETE':
#         blog.delete()
#         return Response({"message": "Deleted successfully"})
