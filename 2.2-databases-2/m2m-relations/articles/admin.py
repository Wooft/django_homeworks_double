from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main') == True:
                count += 1
        if count > 1:
            raise ValidationError('Главным может быть только один тег!')
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    list_filter = ['published_at']
    inlines = [ScopeInline,]



@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['is_main']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']