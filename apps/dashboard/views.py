from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class DashboardView(View):
    def get(self,*args,**kwargs):
        return redirect('user:list_create_profile')
