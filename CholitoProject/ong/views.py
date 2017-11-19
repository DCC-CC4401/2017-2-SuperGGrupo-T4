import locale, datetime, calendar
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from CholitoProject.userManager import get_user_index
from animals.forms import AnimalForm, ImageForm
from animals.models import Animal, AnimalImage
from complaint.models import AnimalType
from naturalUser.models import ONGLike, NaturalUser
from ong.models import ONG


# TODO: use adopt.animal.ong == this_ong to load a notification tab with pending adoptions

class ONGDispatcherView(View):

    context = {'animals': AnimalType.objects.all()}

    def get(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        ong = get_object_or_404(ONG, pk=pk)
        self.context['ong'] = ong
        if c_user.user.has_perm('naturalUser.natural_user_access'):
            self.template_name = 'natural_user_ong.html'
            animals = Animal.objects.filter(ong_id=pk, adoption_state=1)
            self.context['ong_animals'] = animals
            liked = ONGLike.objects.filter(natural_user=c_user, ong=ong).exists()
            self.context['liked'] = liked

        elif c_user.user.has_perm('municipality.municipality_user_access'):

            locale.setlocale(locale.LC_TIME, '')

            dates = []
            date = datetime.date.today()
            for i in range(3):
                dates.append(date)
                date = date.replace(day=1) - datetime.timedelta(days=1)

            # [month, id, quantity, position] = ['enero', 'Esterilizaciones', 80, 1]
            data = []
            position = 0
            for date in reversed(dates):
                month = calendar.month_name[date.month]
                admisions = len(
                    Animal.objects.filter(admission_date__year=date.year, admission_date__month=date.month,
                                          ong=ong))
                # adoptions = len(Animal.objects.filter(adoption_date__year=today.year, adoption_date__month=today.year, ong__pk=1))
                # sterilizations = len(Animal.objects.filter(sterilization_date__year=today.year, sterilization_date__month=today.year, ong__pk=1))

                data.append([month, 'Admisiones', admisions, position])
                # data.append[month, 'Adopciones', adoptions]
                # data.append[month, 'Esterilizaciones', sterilizations]
                position += 1

            self.context['data'] = data
            self.template_name = 'municipality_user_ong.html'

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
    form = AnimalForm(prefix='animal')
    image_form = ImageForm(prefix='image')
    context = {'form': form, 'image_form': image_form}
    template_name = 'add_animal.html'

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user

        return render(request, self.template_name, context=self.context)


class ONGCreateAnimalView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'

    def post(self, request, **kwargs):
        form = AnimalForm(request.POST, request.FILES, prefix='animal')
        image_form = ImageForm(request.POST, request.FILES, prefix='image')
        if form.is_valid():
            animal = form.save(commit=False)
            animal.ong = get_user_index(request.user).ong
            animal.save()
            if image_form.is_valid():
                AnimalImage.objects.create(
                    animal=animal,
                    image=image_form.cleaned_data.get('animal_image'))
        return redirect('ong-index')


class ONGRequestsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'ong.ong_user_access'
    template_name = 'animal_requests.html'
    context = {}

    def get(self, request, pk, **kwargs):
        self.context['animal'] = get_object_or_404(Animal, pk=pk)

        user = get_user_index(request.user)
        requests = NaturalUser.objects.filter(adopt__animal_id=pk,
                                              adopt__animal__ong=user.ong)
        self.context['c_user'] = user
        self.context['users'] = requests

        return render(request, self.template_name, context=self.context)


class ONGFavView(View):
    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        ong = get_object_or_404(ONG, pk=request.GET.get('id'))
        number_of_likes = ong.favourites
        _, created = ONGLike.objects.get_or_create(natural_user=c_user,
                                                   ong=ong)
        if created:
            number_of_likes = ONGLike.objects.filter(
                ong=ong).distinct().count()
            ong.favourites = number_of_likes
            ong.save()

        return HttpResponse(number_of_likes)


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
        self.context['adoptions_days'] = (
            timezone.now() - animal.admission_date).days
        return render(request, self.template_name, context=self.context)


class ONGEditSterilizedStateView(PermissionRequiredMixin, LoginRequiredMixin,
                                 View):
    permission_required = 'ong.ong_user_access'
    template_name = 'edit_animal.html'
    context = {'animals': AnimalType.objects.all()}

    def post(self, request, pk, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        animal = get_object_or_404(Animal, pk=pk)
        animal.is_sterilized = request.POST.get('status')
        animal.save()
        return redirect('edit-animal', pk=pk)
