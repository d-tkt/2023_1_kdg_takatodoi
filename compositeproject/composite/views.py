import re
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Case, When
from .models import RARITY, Item, Composite, Comp_List, Previous_List


class SearchItemView(ListView):
    template_name = 'composite/comp_search.html'
    model = Item

    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            return Item.objects.filter(name__icontains=query)
        else:
            return Item.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context

class DetailCompView(DetailView):
    template_name = 'composite/comp_detail.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_name = self.object.name

        # Composite クラス内で Item クラスの name と一致するレコードを取得
        composite_items = Composite.objects.filter(item__name=item_name)
        use_items = Composite.objects.filter(material__name=item_name)

        context['item_name'] = item_name
        context['composite_items'] = composite_items
        context['use_items'] = use_items
        return context

class CreateItemView(CreateView):
    template_name = 'composite/comp_createitem.html'
    model = Item
    fields = ('name', 'thumbnail', 'rarity')
    success_url = reverse_lazy('index')

class CompositeForm(forms.ModelForm):
    class Meta:
        model = Composite
        fields = ('item', 'material', 'quantity')

    def __init__(self, *args, **kwargs):
        super(CompositeForm, self).__init__(*args, **kwargs)

        # Itemフィールドのクエリセットを設定
        self.fields['item'].queryset = Item.objects.exclude(rarity='中級')

        # Materialフィールドのクエリセットを設定
        self.fields['material'].queryset = Item.objects.exclude(rarity='最上級')

class CreateCompView(CreateView):
    template_name = 'composite/comp_createcomp.html'
    model = Composite
    form_class = CompositeForm
    success_url = reverse_lazy('create-composite')

class DeleteItemView(DeleteView):
    template_name = 'composite/comp_deleteitem.html'
    model = Item
    success_url = reverse_lazy('index')

class ListCompView(ListView):
    template_name = 'composite/comp_listcomp.html'
    model = Composite

class DeleteCompView(DeleteView):
    template_name = 'composite/comp_deletecomp.html'
    model = Composite
    success_url = reverse_lazy('index')

class UpdateItemView(UpdateView):
    template_name = 'composite/comp_updateitem.html'
    model = Item
    fields = ('name', 'thumbnail', 'rarity')
    success_url = reverse_lazy('index')

class UpdateCompView(UpdateView):
    template_name = 'composite/comp_updatecomp.html'
    model = Composite
    fields = ('item', 'material', 'quantity')
    success_url = reverse_lazy('index')

def index_view(request):
    object_list = Item.objects.all()

    # レアリティごとにグループ化
    grouped_items = {
        '最上級': [],
        '上級': [],
        '中級': [],
    }

    for item in object_list:
        grouped_items[item.rarity].append(item)

    return render(request, 'composite/index.html', {'grouped_items': grouped_items})


class CompositeFormView(CreateView):
    model = Comp_List
    fields = ('comp_item', 'comp_quantity')

class CompositeView(ListView):
    template_name = 'composite/comp_composite.html'
    model = Comp_List
    success_url = reverse_lazy('composite-composite')

class CompCompFormView(CompositeFormView, CompositeView):
    def calculate_composite(listData):

        lens = []
        total_materials = []
        for item in listData:
            item_name = item.comp_item
            item_quantity = int(item.comp_quantity)
            flug = False
            item.materials = []
            comp_materials = Composite.objects.filter(item__name=item_name)
            while flug == False:
                if not comp_materials:
                    comp_materials = [""]
                for material in comp_materials:
                    if material == "":
                        material = Item.objects.filter(name=item_name)
                        for i in material:
                            material = i
                        material_name = material
                        material_quantity = 1
                    else:
                        material_name = material.material
                        material_quantity = int(material.quantity)

                    print(material_name.rarity)
                    if material_name.rarity == '中級':
                        existing_material = next((m for m in item.materials if m['material'] == material_name), None)
                        existing_total_material = next((m for m in total_materials if m['material'] == material_name), None)
                        
                        if existing_material:
                            # 同じ素材が既に存在する場合は数量を加算
                            existing_material['quantity'] += material_quantity * item_quantity
                        else:
                            # 新しい素材を追加
                            new_material = {'material': material_name, 'quantity': material_quantity * item_quantity}
                            item.materials.append(new_material)
                        if existing_total_material:
                            existing_total_material['quantity'] += material_quantity * item_quantity
                        else:
                            new_material = {'material': material_name, 'quantity': material_quantity * item_quantity}
                            total_materials.append(new_material)
                        before_materials = item.materials
                        if before_materials == item.materials:
                            lens.append(len(item.materials))
                            flug = True
                    else:
                        plus_materials = Composite.objects.filter(item__name=material_name)
                        comp_materials = comp_materials.exclude(material__name=material_name)
                        comp_materials = comp_materials|plus_materials

        if lens:
            max_len = max(lens)
        else:
            max_len = 0
        for item in listData:
            item.none_len = max_len - len(item.materials)

        return listData, max_len, total_materials

    def get(self, request, *args, **kwargs):
        formView = CompositeFormView.get(self, request, *args, **kwargs)
        formData = formView.context_data['form']
        listview = CompositeView.get(self, request, *args, **kwargs)
        listData = listview.context_data['object_list']

        listData, max_len, total_materials = CompCompFormView.calculate_composite(listData)

        context = {'form': formData, 'object_list': listData, 'max_len': max_len, 'total_materials': total_materials, 'previous': Previous_List.objects.all()}

        return render(request, 'composite/comp_composite.html', context)


def CompCompDelete(request, pk):
    if pk == 0:
        a, a, total_materials = CompCompFormView.calculate_composite(Comp_List.objects.all())
        Previous_List.objects.all().delete()
        for item in total_materials:
            Previous_List.objects.create(previous_item=item['material'], previous_quantity=item['quantity'])
        Comp_List.objects.all().delete()
    else:
        item = get_object_or_404(Comp_List, id=pk)
        item.delete()
    return redirect('composite-composite')
    