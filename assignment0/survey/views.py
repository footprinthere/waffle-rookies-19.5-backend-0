import json
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse, HttpResponseNotAllowed
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from survey.models import SurveyResult, OperatingSystem
from survey.serializers import serialize_survey_result, serialize_os


def get_survey_results(request):
    if request.method == 'GET':
        params = request.GET.get('os')
        if params == None:  # no query paramters
            survey_results = list(map(lambda result: serialize_survey_result(result), SurveyResult.objects.all()))
        else:   # query parameter 'os' exists
            if params not in ('Windows', 'MacOS', 'Ubuntu (Linux)'):
                raise SuspiciousOperation   # 400 Bad Request
            else:
                survey_results = list(map(lambda result: serialize_survey_result(result), SurveyResult.objects.filter(os__name=params)))
        return JsonResponse({"surveys": survey_results}, status=200)
    else:
        return HttpResponseNotAllowed(['GET', ])


def get_survey(request, survey_id):
    if request.method == 'GET':
        survey = get_object_or_404(SurveyResult, id=survey_id)
        return JsonResponse(serialize_survey_result(survey))
    else:
        return HttpResponseNotAllowed(['GET', ])

def get_os_results(request):
    if request.method == 'GET':
        os_results = list(map(lambda result: serialize_os(result), OperatingSystem.objects.all()))
        return JsonResponse({"os" : os_results}, status=200)    
    else:
        return HttpResponseNotAllowed(['GET', ])

def get_os(request, operatingsystem_id):
    if request.method == 'GET':
        try:
            os = OperatingSystem.objects.get(id=operatingsystem_id)
            return JsonResponse(serialize_os(os))
        except OperatingSystem.DoesNotExist:
            raise Http404
    else:
        return HttpResponseNotAllowed(['GET', ])