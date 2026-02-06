from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related("author", "listing").all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
