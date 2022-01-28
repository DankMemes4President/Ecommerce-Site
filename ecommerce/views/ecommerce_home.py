from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from ..models import User, Vendor, Customer


class SignUp(TemplateView):
    template_name = "ecommerce/registration/signup.html"


def home(request):
    if request.user.is_authenticated:
        if request.user.is_vendor:
            return redirect('ecommerce:vendor_dashboard')
        elif request.user.is_customer:
            return redirect('ecommerce:customer_dashboard')
    return render(request, 'ecommerce/index.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('ecommerce:home')


class GoogleUserRoles(TemplateView):
    model = User
    template_name = 'ecommerce/roles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

    def post(self, request):
        user = self.request.user
        if (user.is_customer == False) and (user.is_vendor == False):
            if 'vendor' in request.POST:
                user.is_vendor = True
                user.save()
                vendor = Vendor.objects.create(user=user)
                vendor.save()
                return redirect('ecommerce:vendor_dashboard')
            elif 'customer' in request.POST:
                user.is_customer = True
                user.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                return redirect('ecommerce:customer_dashboard')
        else:
            if user.is_customer:
                return redirect('ecommerce:customer_dashboard')
            elif user.is_vendor:
                return redirect('ecommerce:vendor_dashboard')
