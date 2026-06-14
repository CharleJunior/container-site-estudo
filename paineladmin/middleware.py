from django.shortcuts import redirect
from django.urls import reverse

class ProtectAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:         
            admin_urls = [reverse('admin'), reverse('users')]
            if request.path in admin_urls and not request.user.is_staff:
                return redirect('erro-acesso-negado')

        response = self.get_response(request)
        return response