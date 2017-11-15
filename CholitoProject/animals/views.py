from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from CholitoProject.userManager import get_user_index
from animals.models import Animal, Adopt, AnimalImage
from complaint.models import AnimalType
from naturalUser.models import NaturalUser


class AnimalRenderView(View):
    template_name = 'view_animal.html'
    context = {'animals': AnimalType.objects.all()}

    def get(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user

        animal = get_object_or_404(Animal, pk=pk)
        adopt_users_pk = [adopt.user.pk for adopt in Adopt.objects.filter(animal=animal)]
        self.context['selected_animal'] = animal
        self.context['is_adopter'] = c_user.pk in adopt_users_pk
        self.context['images'] = AnimalImage.objects.filter(animal=animal)
        return render(request, self.template_name, context=self.context)


class AdoptView(View):
    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        animal = get_object_or_404(Animal, pk=request.GET.get('id'))

        Adopt.objects.get_or_create(user=c_user, animal=animal)
        return HttpResponse("")
