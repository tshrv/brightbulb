from django.http import JsonResponse


def gen_response(c_status, c_data=None, c_errors=None):
    return JsonResponse(gen_content(c_status, c_data, c_errors), safe=False, status=c_status)


def gen_content(c_status, c_data=None, c_errors=None):
    c_dict = dict()
    c_dict['status'] = c_status
    if c_data is not None:
        c_dict['data'] = c_data
    if c_errors is not None:
        c_dict['errors'] = c_errors
    return c_dict
