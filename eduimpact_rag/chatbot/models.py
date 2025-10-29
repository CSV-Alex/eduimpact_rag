from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    description = models.TextField(verbose_name="Descripcion")
    context = models.TextField(
        verbose_name="Contexto del Proyecto", 
        help_text="Describe tu proyecto educativo, objetivos, contenido, etc."
    )
    limitations = models.TextField(
        verbose_name="Tus Limitaciones",
        help_text="Recursos limitados, tiempo, nivel de estudiantes, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']