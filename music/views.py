from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.views.generic import UpdateView
from rest_framework import mixins, generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from music.models import Favorite, Comment, MusicImage, Genre, Music, Like, Singer, Review
from music.serializers import FavoriteSongSerializer, CommentSerializer, MusicImageSerialzier, SingerImageSerialzier, \
    GenreSerializer, MusicSerialzier, SingerSerializer, CreateReviewSerializer


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerialzier
    permission_classes = [IsAuthenticated,]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """переопределим данный метод"""
        if self.action in ['update','partial_update','destroy']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    """метод создания лайков"""
    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.is_liked else 'ненравится'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'нравится'
        return Response(message, status=200)


    def get_permission(self):
        if self.action == 'create' or self.action == 'like':
            """Лайки к постам может добавлять только зарегистрированный пользователь"""
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    """метод добавления в избранные"""

    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(post=post, user=user)
            favorite.is_favorite = not favorite.is_favorite
            if favorite.is_favorite:
                favorite.save()
            else:
                favorite.delete()
            message = 'В избранных' if favorite.is_favorite else 'Удалено из избранных'
        except Favorite.DoesNotExist:
            Favorite.objects.create(post=post, user=user, is_favorite=True)
            message = 'Добавлено в избранные'
        return Response(message, status=200)

        def get_permission(self):
            if self.action == 'create' or self.action == 'like' or self.action == 'favorite':
                return [IsAuthenticated()]
            return [IsAuthenticated()]



    """Фильтрацию по дате добавления """
    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('day', 0))
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(weeks=weeks_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    """Создаем метод query params поисковик
    декоратор action работает только с ModelViewSet"""
    @action(detail=False, methods=['get'])    # указываем каким методом будет доступен этот  action
    def search(self, request, pk=None):
        q = request.query_params.get('q')       # query_params то же самое что и request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q)|  # поисковик ищет по ключевым словам в названии и описании
                                   Q(country__icontains=q))    #icontains чтобы фильтр не был чувствителен к регистру
        """| это знак или т.е фильтруй по названию или по тексту"""
        serializer = MusicSerialzier(queryset,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class SingerListView(generics.ListCreateAPIView):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    permission_classes = [AllowAny]


class GenreListView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

class MusicImageView(generics.ListCreateAPIView):
    queryset = MusicImage.objects.all()
    serializer_class = MusicImageSerialzier

    def get_serializer_context(self):
        return {'request': self.request}

class SingerImageView(generics.ListCreateAPIView):
    queryset = MusicImage.objects.all()
    serializer_class = SingerImageSerialzier

    def get_serializer_context(self):
        return {'request': self.request}



class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}




class UpdateCommentView(UpdateView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class DeleteCommentView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentVeiwSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]



class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSongSerializer
    permission_classes = [IsAuthenticated,]















class CreateReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer


class RetrieveUpdateDestroyReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer


