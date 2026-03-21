from django.db import models

class Mural(models.Model):
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)    
