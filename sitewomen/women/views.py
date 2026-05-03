from os import path

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, QueryDict, HttpResponseRedirect, \
    HttpResponsePermanentRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin

# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
#         ]


# Create your views here.
# def index(request):  # HttpRequest
#     posts = Women.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)  # обрабатывает шаблон и отдает его клиенту


# Используется для ЗАРАНЕЕ известных данных (Замена def index)
class WomenHome(DataMixin,ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'  # переменная которая будет содержать список статей
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # для ДИНАМИЧЕСКИХ данных
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# загрузка файлов обязательно в about.html указать атрибут enctype="multipart/form-data"
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})



class ShowPost(DataMixin,DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,title = context['post'].title)


    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[
            self.slug_url_kwarg])  # выбираем из менеджера Вумен Паблишед по слагу (вместо self.slug_url_kwargs можно было указать post_slug)



# добавление записей:
class AddPage(DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'

# редактирование записей:
class UpdatePage(DataMixin,UpdateView):
    model = Women
    fields = ['title','content','photo','is_published','cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")



# замена show_category
class WomenCategory(DataMixin,ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,title = 'Категория - ' + cat.name,cat_selected = cat.pk)


class TagPostList(DataMixin,ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,title = 'Тег - ' + tag.tag)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")
