from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q # Necesitas esto para la búsqueda
from .models import Evento, Categoria


def timeline_view(request):
    """Página principal con la línea de tiempo."""
    categorias = Categoria.objects.all().order_by("nombre")
    return render(request, "lineatiempo/timeline.html", {"categorias": categorias})


def eventos_api(request):
    """Devuelve eventos filtrados y/o buscados como JSON para la timeline."""
    eventos = Evento.objects.all().order_by("year_inicio", "month_inicio", "day_inicio")
    
    # --- 🎯 FILTRO POR CATEGORÍA ---
    # Parámetro esperado: /api/eventos/?category_id=1,2,3
    category_ids = request.GET.get('category_id')
    if category_ids:
        # Convierte "1,2,3" en una lista de IDs [1, 2, 3]
        ids = [int(i) for i in category_ids.split(',') if i.isdigit()]
        if ids:
            eventos = eventos.filter(categoria__id__in=ids)
    
    # --- 🎯 BÚSQUEDA POR TEXTO (Opcional, pero muy bueno) ---
    # Parámetro esperado: /api/eventos/?q=egipto
    query = request.GET.get('q')
    if query:
        # Usa Q object para buscar en título Y descripción
        eventos = eventos.filter(
            Q(titulo__icontains=query) | 
            Q(descripcion__icontains=query)
        )

    # Serializa los eventos restantes (filtrados/buscados)
    data = [e.to_json() for e in eventos]
    return JsonResponse({"events": data})