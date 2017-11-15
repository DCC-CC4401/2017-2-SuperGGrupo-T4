from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from CholitoProject.userManager import get_user_index
from complaint.forms import ComplaintForm, ImageForm
from complaint.models import Complaint, ComplaintImage, AnimalType


class ComplaintView(View):
    form = ComplaintForm(
        initial={'lat': 20, 'lng': 20, 'directions': "beauchef"}, prefix='complaint')
    image_form = ImageForm(prefix='image')
    animals = AnimalType.objects.all()
    context = {'form': form, 'image_form': image_form, 'animals': animals}
    template_name = 'complaint.html'

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user
        return render(request, self.template_name, context=self.context)


class ComplaintSendView(View):

    def post(self, request, **kwargs):
        form = ComplaintForm(request.POST, prefix='complaint')
        image_form = ImageForm(request.POST, request.FILES, prefix='image')
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.status = 1
            complaint.save()
            if image_form.is_valid():
                ComplaintImage.objects.create(
                    complaint=complaint,
                    image=image_form.cleaned_data.get('complaint_image'))

        return redirect('/')


class ComplaintRenderView(PermissionRequiredMixin, LoginRequiredMixin, View):
    template_name = 'view_complaint.html'
    permission_required = 'municipality.municipality_user_access'
    context = {}

    def get(self, request, pk, **kwargs):
        user = get_user_index(request.user)
        self.context['c_user'] = user
        complaint = get_object_or_404(Complaint, pk=pk)
        self.context['complaint'] = complaint

        images = ComplaintImage.objects.filter(complaint=complaint)
        self.context['images'] = images

        return render(request, self.template_name, context=self.context)


class ComplaintActState(PermissionRequiredMixin, LoginRequiredMixin, View):
    template_name = 'view_complaint.html'
    permission_required = 'municipality.municipality_user_access'
    context = {}

    def post(self, request, pk, **kwargs):
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = request.POST['status']
        complaint.save()

        self.context['complaint'] = complaint

        images = ComplaintImage.objects.filter(complaint=complaint)
        self.context['images'] = images
        # render(request, self.template_name, context=self.context)
        return redirect('see-complaint', pk=pk)
