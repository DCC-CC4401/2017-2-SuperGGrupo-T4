from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone

from CholitoProject.userManager import get_user_index
from animals.models import Animal
from complaint.models import AnimalType
from naturalUser.models import ONGLike, NaturalUser
from ong.models import ONG
from animals.models import Animal, Adopt, AnimalImage



# TODO: use adopt.animal.ong == this_ong to load a notification tab with pending adoptions

class ONGNaturalView(View):
    template_name = 'temp_like.html'
    context = {'animals': AnimalType.objects.all()}

    def get(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        ong = get_object_or_404(ONG, pk=pk)
        self.context['ong'] = ong
        number_of_likes = ONGLike.objects.filter(ong=ong).distinct().count()
        self.context['likes'] = number_of_likes
        liked = ONGLike.objects.filter(natural_user=c_user, ong=ong).exists()
        self.context['liked'] = liked

        return render(request, self.template_name, context=self.context)


class ONGIndexView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    template_name = 'ong_for_adoption_main.html'
    context = {}

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        animals = Animal.objects.raw(
            """SELECT "animals_animal"."id", 
            count("animals_adopt"."user_id") AS total FROM "animals_animal" 
            LEFT OUTER JOIN "animals_adopt" 
            ON "animals_animal"."id" = "animals_adopt"."animal_id" 
            WHERE "animals_animal"."ong_id" = %s 
            GROUP BY "animals_animal"."id" """,
            [user.ong.id])

        self.context['animals'] = animals
        self.context['c_user'] = user

        return render(request, self.template_name, context=self.context)


class ONGAdoptedView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    pass


class ONGStatisticsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    pass


class ONGEditView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        if 'avatar' in request.FILES:
            c_user.ong.avatar = request.FILES['avatar']
            c_user.ong.save()
        return redirect('/')


class ONGAddAnimalView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    pass


class ONGRequestsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    template_name = 'animal_requests.html'
    context = {}

    def get(self, request, pk, **kwargs):
        user = get_user_index(request.user)
        requests = NaturalUser.objects.filter(adopt__animal_id=pk,
                                              adopt__animal__ong=user.ong)
        self.context['c_user'] = user
        self.context['users'] = requests

        return render(request, self.template_name, context=self.context)

class ONGEditAnimalView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    template_name = 'edit_animal.html'
    context = {'animals': AnimalType.objects.all()}

    def get(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user

        animal = get_object_or_404(Animal, pk=pk)
        self.context['selected_animal'] = animal
        self.context['images'] = AnimalImage.objects.filter(animal=animal)
        self.context['adoptions_days'] = (timezone.now() - animal.admission_date).days
        return render(request, self.template_name, context=self.context)

class ONGEditSterilizedStateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    template_name = 'edit_animal.html'
    context = {'animals': AnimalType.objects.all()}

    def post(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        animal = get_object_or_404(Animal, pk=pk)
        animal.is_sterilized = request.POST.get('status')
        animal.save()
        self.context['selected_animal'] = animal
        self.context['images'] = AnimalImage.objects.filter(animal=animal)
        self.context['adoptions_days'] = (timezone.now() - animal.admission_date).days

        return redirect('edit-animal', pk=pk)
    
