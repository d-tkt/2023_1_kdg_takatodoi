from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q, Case, When
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator

from .models import Dictionary
from .consts import ITEM_PER_PAGE


class ListDicView(ListView):
    template_name = 'dictionary/dictionary_list.html'
    model = Dictionary

    paginate_by = ITEM_PER_PAGE


class DetailDicView(DetailView):
    template_name = 'dictionary/dictionary_detail.html'
    model = Dictionary

    def get_object(self, queryset=None):
        # URLからtitleを取得
        title = self.kwargs.get('title')
        # titleを元に対象のオブジェクトを取得
        return get_object_or_404(Dictionary, title=title)


class CreateDicView(CreateView):
    template_name = 'dictionary/dictionary_create.html'
    model = Dictionary
    fields = ('title', 'member', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('index')


class DeleteDicView(DeleteView):
    template_name = 'dictionary/dictionary_delete.html'
    model = Dictionary
    success_url = reverse_lazy('index')


class UpdateDicView(UpdateView):
    template_name = 'dictionary/dictionary_update.html'
    model = Dictionary
    fields = ('title', 'member', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        # URLからtitleを取得
        title = self.kwargs.get('title')
        # titleを元に対象のオブジェクトを取得
        obj = get_object_or_404(Dictionary, title=title)
        return obj


class SearchDicView(ListView):
    template_name = 'dictionary/dictionary_search.html'
    model = Dictionary

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            return Dictionary.objects.filter(Q(title__icontains=query) | Q(text__icontains=query) | Q(member__icontains=query)).order_by("title", "member", "text")
        else:
            return Dictionary.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context


class CategoryDicView(ListView):
    template_name = 'dictionary/dictionary_category.html'
    model = Dictionary

    def get_queryset(self):
        category = self.kwargs['category']
        query = self.request.GET.get('query')

        if query:
            return Dictionary.objects.filter(Q(title__icontains=query) | Q(text__icontains=query) | Q(member__icontains=query), category=category)
        else:
            return Dictionary.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        context['search_query'] = self.request.GET.get('query', '')
        return context


def index_view(request):
    object_list = Dictionary.objects.all()

    paginator = Paginator(object_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request, 'dictionary/index.html', {'page_obj':page_obj})
