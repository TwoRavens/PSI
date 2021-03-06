import json
import requests
import urllib.parse

from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
#from psiproject.settings.local import ROOK_SVC_URL
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from psi_apps.utils.view_helper import \
    (get_json_error, get_json_success)

@login_required(login_url='login')
def view_rook_route(request, app_name_in_url):
    """Route the call to Rook and back"""

    rook_svc_url = '{0}{1}'.format(settings.ROOK_SERVER_BASE, app_name_in_url)

    decode = request.body.decode('utf-8')

    data_payload = {'tableJSON': decode}

    print('rook_svc_url', rook_svc_url)
    try:
        rservice_req = requests.post(rook_svc_url, data=data_payload)
    except ConnectionError:
        user_msg = 'R Server not responding: %s' % rook_svc_url
        print('err_msg', user_msg)
        return JsonResponse(get_json_error(user_msg))


    print('status code from rook call: %d' % rservice_req.status_code)

    print('rservice_req text', rservice_req.text)

    try:
        json_info = rservice_req.json()
    except json.decoder.JSONDecodeError as ex_obj:
        user_msg = 'rook response is not JSON. Error: %s' % ex_obj
        return JsonResponse(get_json_error(user_msg))

    # current
    #
    #if app_name_in_url not in ['privateStatisticsapp']:
    #     return JsonResponse(json_info)

    # preferable, need UI to handle
    #
    user_resp = get_json_success('success',
                                 data=json_info)
    return JsonResponse(user_resp)


@login_required(login_url='login')
def download_rook_route(request, filename):
    """Route the call to Rook and back"""

    print('filename', filename)

    rook_svc_url = '{0}{1}{2}'.format(settings.ROOK_SERVER_BASE, 'rook-files/', filename)

    print('rook_svc_url download', rook_svc_url)
    try:
        rservice_req = requests.get(rook_svc_url)
    except ConnectionError:
        user_msg = 'R Server not responding: %s' % rook_svc_url
        print('err_msg', user_msg)
        return JsonResponse(get_json_error(user_msg))


    print('status code from rook call: %d' % rservice_req.status_code)

    # print('rservice_req content', rservice_req.content)

    return HttpResponse(
        rservice_req.content,
        status=rservice_req.status_code,
        content_type=rservice_req.headers['Content-Type'])
