from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)



class Post(admin.ModelAdmin):
    list_display=['title','slug','author','publish']
    list_filter = ['created', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    show_facets= admin.ShowFacets.ALWAYS
