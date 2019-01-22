from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS #登入驗證 
from rest_framework import mixins, status

from .models import Post, Commit
from .permissions import IsCreatorOrReadOnly, CanUpdateOrDeleteCommit
from .serializers import PostSerializer, CommitsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly] #驗證    

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.action == 'commit': 
            return CommitsSerializer

        return serializer
            
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

    @action(['PATCH'], True, permission_classes = [IsAuthenticated])
    def like(self, request, pk):
        post = self.get_object()

        if request.user in post.likes.all():  #如果使用者在這篇文已按讚的人集合當中
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(['POST'], True, permission_classes = [IsAuthenticated])
    def commit(self, request, pk):
        post =self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=self.request.user, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    

class CommitViewSet(viewsets.ModelViewSet):
    queryset = Commit.objects.all()
    serializer_class = CommitsSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)

    @action(['PATCH'], True, permission_classes = [IsAuthenticated, CanUpdateOrDeleteCommit])
    def like(self, request, pk):
        commit = self.get_object()

        if request.user in commit.likes.all():  #如果使用者在這篇文已按讚的人集合當中
            commit.likes.remove(request.user)
        else:
            commit.likes.add(request.user)

        serializer = self.get_serializer(commit)
        return Response(serializer.data)