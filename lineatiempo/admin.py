from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.http import JsonResponse
from django.urls import path
from .models import Categoria, Evento


# ----------------------
# WIDGET PARA COLOR
# ----------------------
class ColorWidget(forms.TextInput):
    input_type = 'color'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'style': 'width: 80px; height: 40px; padding: 0; border: none;'
        })


# ----------------------
# FORM DE CATEGORIA
# ----------------------
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'color': ColorWidget(),
        }


# ----------------------
# ADMIN DE CATEGORIA
# ----------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm
    list_display = ('nombre', 'color', 'color_muestra')
    search_fields = ('nombre',)

    def color_muestra(self, obj):
        return format_html(
            '<div style="width: 40px; height: 20px; background:{}; border:1px solid #000;"></div>',
            obj.color
        )


# ----------------------
# FORM DE EVENTO
# ----------------------
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'color': ColorWidget(),
        }
    class Media:
        js = ('lineatiempo/evento_auto_color.js',)  # ruta correcta


# ----------------------
# ADMIN DE EVENTO
# ----------------------
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    form = EventoForm
    list_display = ('titulo', 'year_inicio', 'year_fin', 'categoria', 'color_muestra')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descripcion')
    ordering = ('year_inicio', 'month_inicio', 'day_inicio')

    # URL personalizada para obtener color por AJAX
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'get_categoria_color/<int:pk>/',
                self.admin_site.admin_view(self.get_categoria_color),
                name='lineatiempo_get_categoria_color',
            ),
        ]
        return custom_urls + urls

    # Devuelve el color de una categoría
    def get_categoria_color(self, request, pk):
        try:
            cat = Categoria.objects.get(pk=pk)
            return JsonResponse({'color': cat.color})
        except Categoria.DoesNotExist:
            return JsonResponse({'color': None})

    # columna COLOR en el listado
    def color_muestra(self, obj):
        return format_html(
            '<div style="width: 40px; height: 20px; background:{}; border:1px solid #000;"></div>',
            obj.color
        )
