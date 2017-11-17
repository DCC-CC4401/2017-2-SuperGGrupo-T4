from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from CholitoProject.userManager import get_user_index
from animals.models import Animal
from complaint.models import AnimalType
from naturalUser.models import ONGLike
from ong.models import ONG


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
    template_name = 'ong_for_adoption.html'
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

        return render(request, self.template_name, context=self.context)

# TODO: use adopt.animal.ong == this_ong to load a notification tab with pending adoptions
