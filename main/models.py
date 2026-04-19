from django.db import models
from django.contrib.auth.models import User
class Mural(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now=True) # Atualiza a data sozinho
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mural_main')

    def __str__(self):
        return f"Aviso de {self.autor.username if self.autor else 'Sistema'}"  



