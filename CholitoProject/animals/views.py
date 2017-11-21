from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View

from CholitoProject.userManager import get_user_index
from animals.models import Animal, Adopt, AnimalImage
from complaint.models import AnimalType


class AnimalRenderView(View):
    template_name = 'view_animal.html'
    context = {'animals': AnimalType.objects.all()}

    def get(self, request, pk, **kwargs):
        animal = get_object_or_404(Animal, pk=pk)
        self.context['selected_animal'] = animal
        self.context['images'] = AnimalImage.objects.filter(animal=animal)
        self.context['adoptions_days'] = (
            timezone.now().date() - animal.admission_date).days
        c_user = get_user_index(request.user)
        if c_user:
            self.context['c_user'] = c_user
            is_adopter = Adopt.objects.filter(animal=animal,
                                              user=c_user).exists()
            self.context['is_adopter'] = is_adopter

        return render(request, self.template_name, context=self.context)


class AdoptView(View):
    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        animal = get_object_or_404(Animal, pk=request.GET.get('id'))
        Adopt.objects.get_or_create(user=c_user, animal=animal)
        return HttpResponse("")
