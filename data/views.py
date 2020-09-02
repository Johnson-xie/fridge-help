from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import layer_map


@api_view(['GET'])
def get_temperature(request):
    start = request.query_params.get('start', '2020-01-01 00:00:00')
    end = request.query_params.get('end', '2099-12-31 00:00:00')

    sql = '''
            SELECT 
                code, GROUP_CONCAT(time) AS time, GROUP_CONCAT(value ) AS value 
            FROM 
                tbl_temperature 
            WHERE 
                time>=%s AND time<=%s 
            GROUP BY 
                code 
            ORDER BY 
                `time`
    '''
    with connection.cursor() as c:
        c.execute(sql, (start, end))
        rows = c.fetchall()

    data = []
    for code, t, values in rows:
        data.append(
            {
                'code': layer_map[code],
                'time': t.split(','),
                'value': values.split(',')
            }
        )
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_power(request):
    start = request.query_params.get('start', '2020-01-01 00:00:00')
    end = request.query_params.get('end', '2099-12-31 00:00:00')

    sql = "select time, voltage, current, rate, consumption from tbl_power where time>=%s and time<=%s order by time"
    with connection.cursor() as c:
        c.execute(sql, (start, end))
        rows = c.fetchall()
    time_list, voltage_list, current_list, rate_list, consumption_list = [], [], [], [], []
    for time, voltage, current, rate, consumption in rows:
        time_list.append(time)
        voltage_list.append(voltage)
        current_list.append(current)
        rate_list.append(rate)
        consumption_list.append(consumption)

    data = {
        'time': time_list,
        'voltage': voltage_list,
        'current': current_list,
        'rate': rate_list,
        'consumption': consumption_list
    }
    return Response(data=data, status=status.HTTP_200_OK)
