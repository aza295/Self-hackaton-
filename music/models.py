from django.db import models
from datetime import date
from registration.models import User






class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Singer(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вокалист"
        verbose_name_plural = "Вокалист"


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Music(models.Model):
    """Музыка"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    genres = models.ForeignKey(Genre, related_name='genres', on_delete=models.CASCADE)
    authors = models.ForeignKey(Singer, related_name='singers', on_delete=models.CASCADE)
    draft = models.BooleanField("Черновик", default=False)

    class Meta:
        verbose_name = 'Песню'
        verbose_name_plural = 'Песня'

    def __str__(self):
        return self.title

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


""" Создаем модель для загрузки картинок"""
class MusicImage(models.Model):
    image = models.ImageField(upload_to='music',blank=True,null=True)
    post = models.ForeignKey(Music, on_delete=models.CASCADE,related_name='image')


""" Создаем модель для загрузки картинок"""
class SingerImage(models.Model):
    images = models.ImageField(upload_to='singer',blank=True,null=True)
    post = models.ForeignKey(Singer, on_delete=models.CASCADE,related_name='images')


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Создаем модель Коммент"""
class Comment(models.Model):
    post = models.ForeignKey(Music,
                                    on_delete=models.CASCADE,
                                    related_name='comments',
                                    verbose_name='Публикация')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Автор')
    text = models.TextField('Текст',)
    created_at = models.DateTimeField('Дата создания',auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post} -->{self.user}'

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


""" Создаем модель лайка"""
class Like(models.Model):
    post = models.ForeignKey(Music,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)



class Favorite(models.Model):
    post = models.ForeignKey(Music , on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    is_favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()




class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    music = models.ForeignKey(Music,
                                on_delete=models.CASCADE,
                                verbose_name='Песня')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                                            verbose_name='Рейтинг')

    def avr_rating(self):
        summ = 0
        ratings = Review.objects.filter(post=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return summ / len(ratings)
        else:
            return 'Нет рейтинга'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

    def __str__(self):
        return f'Пост: {self.music}, Автор: {self.author}'