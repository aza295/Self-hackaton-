
from rest_framework import serializers
from rest_framework.utils import representation

from music.models import Genre, Music, Comment, Favorite, MusicImage, SingerImage, Singer, Review


class MusicSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('title','description','year','country','draft')

    """def to_representation отвечает за то в каком виде возвращается(Переопределяет) Responce"""

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(dir(instance))
        representation['authors'] = SingerSerializer(instance.authors).data
        representation['genre'] = GenreSerializer(instance.genres).data
        representation['likes'] = instance.likes.count()
        representation['images'] = SingerImageSerialzier(instance.images.all(),many=True).data
        representation['review'] = ReviewDetailSerializer(instance.review_set.all(), many=True).data
        representation['image'] = MusicImageSerialzier(instance.image.all(), many=True,
                                                       context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        authors = request.user.id
        post = Music.objects.create(**validated_data)
        return post



""" Создаем сериализатор который будет добавлять коментарии"""
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True,
                                                     queryset=Music.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


""" Создаем сериализатор который будет отображать Жанры"""
class GenreSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only =True) # Будет показывать дату создания
    """ class Meta - Это просто контейнер класса с некоторыми параметрами(метаданными), прикрепленными к модели"""
    class Meta:
        model = Genre
        fields = '__all__'

class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'


class MusicImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = MusicImage
        fields = '__all__'

    def get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                ulr = ''
            return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['images'] = self.get_image_url(instance)
        return representation

class SingerImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = SingerImage
        fields = '__all__'

    def get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                ulr = ''
            return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['images'] = self.get_image_url(instance)
        return representation




class MusicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True,
                                                     queryset=Music.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class FavoriteSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('post',)

    def get_favorite(self, obj,request):
        if obj.favorite and request.user and request.user == obj.user:
            return obj.favorite
        return ''































class CreateReviewSerializer(serializers.ModelSerializer):
    music = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Music.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        music = attrs.get('post')
        request = self.context.get('request')
        author = request.user
        if Review.objects.filter(music=music, author=author).exists():
            raise serializers.ValidationError('Невозможно поставить рейтинг дважды')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)




class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


