from django.contrib import admin
from .models import Post, Category, Tag, Comment # Post 모델을 불러옴
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post, MarkdownxModelAdmin) # Post 모델을 관리자 페이지에서 볼 수 있도록 등록

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # name 하고 ',' 붙는이유가 튜플로 생성하려고 하는데 변경안되게 하려고..
    # 튜플로 안해도 생성은 되겠지만 문제가 생길 수 있음.

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag, TagAdmin)