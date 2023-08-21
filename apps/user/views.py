from typing import Any, Dict
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Customer
from .forms import CreateProfileForm


class ListCreateProfileView(FormView):
    template_name = 'auth/register.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy("user:list_create_profile")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["users"]=Customer.objects.all()
        print(context)
        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
