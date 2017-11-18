from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from CholitoProject.userManager import get_user_index
from complaint.models import AnimalType
from naturalUser.forms import SignUpForm, AvatarForm
from naturalUser.models import NaturalUser


class IndexView(TemplateView):
    context = {}

    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        animals = AnimalType.objects.all()
        self.context['animals'] = animals
        if c_user is None:
            return render(request, 'index.html', context=self.context)
        return c_user.get_index(request, context=self.context)


class LogInView(TemplateView):
    template_name = 'login.html'
    animals = AnimalType.objects.all()
    context = {'animals': animals}

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.context)


class SignUpView(View):
    user_form = SignUpForm(initial={'username': 'dummy'}, prefix='user')
    avatar_form = AvatarForm(prefix='avatar')
    animals = AnimalType.objects.all()
    context = {'user_form': user_form,
               'avatar_form': avatar_form, 'animals': animals}
    template_name = 'sign_up.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.context)

    def post(self, request, **kwargs):
        user_form = SignUpForm(request.POST, prefix='user')
        avatar_form = AvatarForm(request.POST, request.FILES, prefix='avatar')
        if user_form.is_valid() and avatar_form.is_valid():
            user_ = user_form.save()
            user_.refresh_from_db()
            avatar_ = avatar_form.cleaned_data.get('avatar')
            if avatar_ is None:
                natural_user = NaturalUser.objects.create(
                    user=user_)
            else:
                natural_user = NaturalUser.objects.create(
                    user=user_, avatar=avatar_)
            username = user_form.cleaned_data.get('email')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        messages.error(request,
                       "Ha ocurrido un error en el registro. Debes ingresar todos los campos para registrarse")
        return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'naturalUser.natural_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        c_user.user.first_name = request.POST['f_name']
        c_user.user.last_name = request.POST['l_name']
        if 'avatar' in request.FILES:
            c_user.avatar = request.FILES['avatar']
        c_user.save()
        return redirect('/')


class ONGListView(View):
    pass


class AnimalListView(View):
    pass
