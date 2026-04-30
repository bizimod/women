from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщик'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('singe', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'singe':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo','post_photo', 'cat', 'husband', 'tags']  # список полей отображаемых в админке
    # exclude = ('tags','is_published') # исключить поля из отображаемых
    readonly_fields = ['post_photo'] # поля недоступные для редакции
    prepopulated_fields = {
        "slug": ("title",)}  # автоматически формирует слаг. Поле слаг обязательно должно быть редактируемым!!!
    # filter_horizontal = ('tags',)  # изменение вида поля тегов
    filter_vertical = ('tags',)  # аналог горизонтал
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')  # список полей
    list_display_links = ('title',)  # кликабельные поля
    ordering = ('-time_create', 'title',)
    list_editable = ('is_published',)  # поля доступные для редактирования (не могут быть кликабельными)
    list_per_page = 10  # настраивается количество элементов списка на странице
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']  # поля по которым будет происходить поиск
    list_filter = (MarriedFilter, 'cat__name', 'is_published')  # добавление фильтра в админ панель
    save_on_top = True

    @admin.display(description='Изображение', ordering=('content'))  # добавление нового поля которого нет в бд
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено  {count} записей.')

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей сняты с публикации.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # список полей
    list_display_links = ('id', 'name')  # кликабельные поля



