

from django.contrib import admin

from music.models import Genre, Singer, Music, Comment, MusicImage, SingerImage


class MusicImageInline(admin.TabularInline):
    model = MusicImage
    max_num = 10
    min_num = 1

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    inlines = [MusicImageInline,]


class SingerImageInline(admin.TabularInline):
    model = SingerImage
    max_num = 10
    min_num = 1

@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    inlines = [SingerImageInline,]

admin.site.register(Genre)
admin.site.register(Comment)





