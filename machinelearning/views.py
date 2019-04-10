from django.http import JsonResponse
from django.conf import settings
from rest_framework import status

import pandas as pd
from sklearn.externals import joblib

import os
from datetime import datetime


def load_regressor(filename):
    file = os.path.join(settings.BASE_DIR, filename)
    return joblib.load(file)


# VIEW
def make_prediction(request, date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        content = {
            'status': status.HTTP_406_NOT_ACCEPTABLE,
            'data': {
                'date': date_str,
                'error': 'Date should be in format YYYY-MM-DD',
            }
        }
        return JsonResponse(content, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)

    yday = pd.Series(date.timetuple().tm_yday).values.reshape(-1, 1)

    tmin_rgr = load_regressor('regressors/tmin_regressor.rgr')
    tmax_rgr = load_regressor('regressors/tmax_regressor.rgr')
    tavg_rgr = load_regressor('regressors/tavg_regressor.rgr')
    content = {
        'status': status.HTTP_200_OK,
        'data': {
            'date': date_str,
            'tmin': tmin_rgr.predict(yday)[0][0],
            'tmax': tmax_rgr.predict(yday)[0][0],
            'tavg': tavg_rgr.predict(yday)[0][0],
        }
    }
    return JsonResponse(content, safe=False, status=status.HTTP_200_OK)
