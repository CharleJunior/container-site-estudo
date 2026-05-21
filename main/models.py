from django.db import models
from django.contrib.auth.models import User
class Mural(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now=True) # Atualiza a data sozinho
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mural_main')

    def __str__(self):
        return f"Aviso de {self.autor.username if self.autor else 'Sistema'}"

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_envio']


class notificacao(models.Model):
   usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
   mensagem_corpo = models.ForeignKey(Mensagem, on_delete=models.CASCADE)
   lida = models.BooleanField(default=False)
   data_criacao = models.DateTimeField(auto_now_add=True)
   class Meta:
       ordering = ['-data_criacao']