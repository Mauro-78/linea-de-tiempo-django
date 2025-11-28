from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(
        max_length=20,
        default="#1f77b4",
        help_text="Color en formato HEX (ej: #1f77b4)",
    )
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    # Año puede ser negativo → AC  (ej: -1513 = 1513 a.C.)
    year_inicio = models.IntegerField(
        "Año inicio",
        help_text="Ej: -1513 = 1513 a.C., 2024 = 2024 d.C."
    )
    month_inicio = models.PositiveSmallIntegerField(
        "Mes inicio", blank=True, null=True, help_text="1-12 (opcional)"
    )
    day_inicio = models.PositiveSmallIntegerField(
        "Día inicio", blank=True, null=True, help_text="1-31 (opcional)"
    )

    # Fin opcional
    year_fin = models.IntegerField("Año fin", blank=True, null=True)
    month_fin = models.PositiveSmallIntegerField("Mes fin", blank=True, null=True)
    day_fin = models.PositiveSmallIntegerField("Día fin", blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos",
    )

    color = models.CharField(
        max_length=20,
        default="#1f77b4",
        help_text="Color del evento (por defecto usa el de la categoría)",
    )
    imagen = models.URLField(
        blank=True,
        null=True,
        help_text="URL opcional de una imagen relacionada"
    )

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["year_inicio", "month_inicio", "day_inicio"]

    def __str__(self):
        return self.titulo

    # --- helpers para la API ---

    def _fecha_dict(self, year, month, day):
        """Devuelve un diccionario con año/mes/día (mes/día opcionales)."""
        if year is None:
            return None
        return {
            "year": year,
            "month": month or 1,
            "day": day or 1,
        }

    def to_json(self):
        """Formato que va a consumir el JavaScript de la timeline."""
        cat = self.categoria
        color = self.color or (cat.color if cat else "#1f77b4")

        return {
            "id": self.id,
            "title": self.titulo,
            "text": self.descripcion or "",
            "start": self._fecha_dict(self.year_inicio, self.month_inicio, self.day_inicio),
            "end": self._fecha_dict(self.year_fin, self.month_fin, self.day_fin),
            "category": cat.nombre if cat else "Sin categoría",
            "category_id": cat.id if cat else None,
            "color": color,
            "image": self.imagen or "",
        }
