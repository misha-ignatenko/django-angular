# -*- coding: utf-8 -*-
import json
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from djangular.views.partials import DjngPartialViewMixin
from server.forms import SubscriptionFormWithNgValidation, SubscriptionFormWithNgModel, SubscriptionFormWithNgValidationAndModel


class SubscribeFormView(TemplateView):
    def get_context_data(self, form=None, **kwargs):
        context = super(SubscribeFormView, self).get_context_data(**kwargs)
        form.fields['height'].widget.attrs['step'] = 0.05  # Ugly hack to set step size
        context.update(form=form)
        return context

    def get(self, request, **kwargs):
        form = self.form()
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        if request.is_ajax():
            return self.ajax(request.body)
        form = self.form(request.POST)
        if form.is_valid():
            return redirect('form_data_valid')
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    def ajax(self, request_body):
        in_data = json.loads(request_body)
        form = self.form(data=in_data)
        response_data = {'errors': form.errors}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class SubscribeViewWithFormValidation(SubscribeFormView):
    template_name = 'subscribe-form.html'
    form = SubscriptionFormWithNgValidation


class SubscribeViewWithModelForm(SubscribeFormView):
    template_name = 'model-form.html'
    form = SubscriptionFormWithNgModel


class SubscribeViewWithModelFormAndValidation(SubscribeFormView):
    template_name = 'model-validation-form.html'
    form = SubscriptionFormWithNgValidationAndModel


class Ng3WayDataBindingView(SubscribeViewWithModelForm):
    template_name = 'three-way-data-binding.html'


class NgFormDataValidView(TemplateView):
    """
    This view just displays a success message, when a valid form was posted successfully.
    """
    template_name = 'form-data-valid.html'


class PartialsView(DjngPartialViewMixin, TemplateView):
    """
    This view demonstrates how to work with partials.
    """
    template_name = 'partial-home.html'
    ng_routes = {
        'list': {'controller': 'ListCtrl', 'templateUrl': 'partial-demo/partialA.html'},
        'detail': {'controller': 'DetailCtrl', 'templateUrl': 'partial-demo/partialB.html'},
        None: {'controller': 'DefaultCtrl', 'templateUrl': 'partial-demo/defaultPartial.html'},
    }

    def get_context_data(self, form=None, **kwargs):
        context = super(PartialsView, self).get_context_data(**kwargs)
        return context
