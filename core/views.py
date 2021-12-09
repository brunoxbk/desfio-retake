from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from core.models import Process, Part
from django.views.generic.list import ListView
from core.forms import ProcessForm, PartFormSet, SearchForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class ProcessList(ListView):
    model = Process

    def get_queryset(self, **kwargs):
        queryset = Process.objects.all()
        if self.request.GET.get('search', None):
            queryset = queryset.filter(parts__id=self.request.GET['search'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProcessList, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class ProcessCreate(View):
    form_class = ProcessForm
    formset_class = PartFormSet
    template_name = 'core/process_form.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['form'] = self.form_class()
        context['formset'] = self.formset_class(queryset=Part.objects.none())
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            process = form.save()

            for form in formset:
                if form.is_valid():

                    if form.cleaned_data.get('DELETE', None) and form.instance.pk:
                        form.instance.delete()
                    else:
                        part = form.save(commit=False)
                        part.process = process
                        part.save()
            messages.success(request, "Processo salvo")
            return HttpResponseRedirect(reverse_lazy('core:list'))

        return render(request, self.template_name, {'form': form, 'formset': formset})


class ProcessUpdate(View):
    form_class = ProcessForm
    formset_class = PartFormSet
    template_name = 'core/process_form.html'

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Process, pk=pk)
        context = dict()
        context['form'] = self.form_class(instance=instance)
        context['formset'] = self.formset_class(queryset=instance.parts.all())
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Process, pk=pk)
        form = self.form_class(instance=instance, data=request.POST)
        formset = self.formset_class(
            queryset=instance.parts.all(), data=request.POST)
        if form.is_valid() and formset.is_valid():
            process = form.save()

            for form in formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE', None) and form.instance.pk:
                        form.instance.delete()
                    else:
                        part = form.save(commit=False)
                        part.process = process
                        part.save()
            messages.success(request, "Processo salvo")
            return HttpResponseRedirect(reverse_lazy('core:list'))

        return render(request, self.template_name, {'form': form, 'formset': formset})


class ProcessDelete(DeleteView):
    model = Process
    success_url = reverse_lazy('core:list')


class ProcessDetail(DetailView):
    model = Process


class SearchPart(View):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', None)
        if term:
            result = Part.objects.filter(
                name__icontains=term).values('id', 'name')
        else:
            result = []

        return JsonResponse({'result': list(result)})
