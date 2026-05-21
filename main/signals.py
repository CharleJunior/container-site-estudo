from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mensagem

@receiver(post_save, sender=Mensagem)
def criar_notificacao(sender, instance, created, **kwargs):
    if created:
        from .models import notificacao
        notificacao.objects.create(
            usuario=instance.destinatario,
            mensagem_corpo=instance
            )