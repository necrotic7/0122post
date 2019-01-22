from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS #登入驗證 


from .models import Post
from .permissions import IsCreatorOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly] #驗證    

    # def get_serializer_class(self):
    #     serializer = super().get_serializer_class()
    #     if self.request.method in SAFE_METHODS: #如果方法安全
    #         return CreatePostSerializer

    #     return serializer
            
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

    @action(['PATCH'], True)
    def like(self, request, pk):
        post = self.get_object()

        if request.user in post.likes.all():  #如果使用者在這篇文已按讚的人集合當中
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)