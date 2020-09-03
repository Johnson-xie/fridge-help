import datetime
import random
from itertools import groupby

from django.db import connection
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader
from pyecharts.charts import Bar, Grid, Line, Kline
from pyecharts.faker import Faker
from pyecharts.globals import CurrentConfig
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./data/templates"))

from pyecharts import options as opts
from pyecharts import charts

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


def index(request):
    c = (
        charts.Line()
            .add_xaxis([i for i in range(1000)])
            .add_yaxis("商家A", [random.randint(50, 100) for i in range(1000)])
            .add_yaxis("商家B", [random.randint(1, 50) for i in range(1000)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return HttpResponse(c.render_embed())


def draw_power(request):
    start = request.GET.get('day')

    if not start:
        start = datetime.date.today()
    else:
        try:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        except:
            start = datetime.date.today()
    end = start + datetime.timedelta(days=1)

    sql = "select time, voltage, current, rate, consumption from tbl_power where time>=%s and time<%s order by time"
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

    c = (
        charts.Line()
            .add_xaxis(time_list)
            .add_yaxis("电压", voltage_list)
            .add_yaxis("电流", current_list)
            .add_yaxis("功率", rate_list)
            .add_yaxis("累计耗电量", consumption_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="测试监控", subtitle="耗电基本信息"))
    )
    return HttpResponse(c.render_embed())


def draw_temperature(request):
    start = request.GET.get('day')

    if not start:
        start = datetime.date.today()
    else:
        try:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        except:
            start = datetime.date.today()
    end = start + datetime.timedelta(days=1)

    sql = 'SELECT time, code, value FROM  tbl_temperature where time>=%s AND time<%s order by code, time'
    with connection.cursor() as c:
        c.execute(sql, (start, end))
        rows = c.fetchall()

    time_list = []
    lines = []

    for key, content in groupby(rows, key=lambda x: x[1]):
        if not time_list:
            values = []
            for time, _, value in content:
                time_list.append(time)
                values.append(value)
        else:
            values = [value for _, _, value in content]
        lines.append((layer_map[key], values))

    if len(lines) != 6:
        c = (
            charts.Line()
                .add_xaxis(time_list)
                .add_yaxis("传感器异常", [])
                .set_global_opts(title_opts=opts.TitleOpts(title="测试监控", subtitle="传感器温度信息"))
        )
    else:
        c = (
            charts.Line()
                .add_xaxis(time_list)
                .add_yaxis(lines[0][0], lines[0][1])
                .add_yaxis(lines[1][0], lines[1][1])
                .add_yaxis(lines[2][0], lines[2][1])
                .add_yaxis(lines[3][0], lines[3][1])
                .add_yaxis(lines[4][0], lines[4][1])
                .add_yaxis(lines[5][0], lines[5][1])
                .set_global_opts(title_opts=opts.TitleOpts(title="测试监控", subtitle="传感器温度信息"))
        )
    return HttpResponse(c.render_embed())


def draw_action(request):
    start = request.GET.get('day')

    if not start:
        start = datetime.date.today()
    else:
        try:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        except:
            start = datetime.date.today()
    end = start + datetime.timedelta(days=1)

    sql = "select time, yaw, pitch, roll, acc_x, acc_y, acc_z from tbl_door where time>=%s and time<%s order by time"
    with connection.cursor() as c:
        c.execute(sql, (start, end))
        rows = c.fetchall()
    time_list, yaw_list, pitch_list, roll_list, accx_list, accy_list, accz_list = [[] for _ in range(7)]
    for time, yaw, pitch, roll, acc_x , acc_y, acc_z in rows:
        time_list.append(time)
        yaw_list.append(yaw)
        roll_list.append(roll)
        accx_list.append(acc_x)
        accy_list.append(acc_y)
        accz_list.append(acc_z)

    c = (
        charts.Line()
            .add_xaxis(time_list)
            .add_yaxis("yaw", yaw_list)
            .add_yaxis("pitch", pitch_list)
            .add_yaxis("roll", roll_list)
            .add_yaxis("x向加速度", accx_list)
            .add_yaxis("y向加速度", accy_list)
            .add_yaxis("z向加速度", accz_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="测试监控", subtitle="门的开关监控数据流"))
    )
    return HttpResponse(c.render_embed())


def draws(request):

    start = request.GET.get('day')

    if not start:
        start = datetime.date.today()
    else:
        try:
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        except:
            start = datetime.date.today()
    end = start + datetime.timedelta(days=1)

    power_sql = 'SELECT DATE_FORMAT(time, "%%Y-%%m-%%d %%H:%%i:%%S") as time, voltage, current, rate, consumption from tbl_power where time>=%s and time<%s order by time'
    temp_sql = 'SELECT DATE_FORMAT(time, "%%Y-%%m-%%d %%H:%%i:%%S") as time, code, value FROM  tbl_temperature where time>=%s AND time<%s order by code, time'
    action_sql = 'SELECT DATE_FORMAT(time, "%%Y-%%m-%%d %%H:%%i:%%S") as time, yaw, pitch, roll, acc_x, acc_y, acc_z from tbl_door where time>=%s and time<%s order by time'

    with connection.cursor() as c:
        c.execute(power_sql, (start, end))
        power_rows = c.fetchall()

        c.execute(temp_sql, (start, end))
        temp_rows = c.fetchall()

        c.execute(action_sql, (start, end))
        action_rows = c.fetchall()

    time_list, voltage_list, current_list, rate_list, consumption_list = [[] for _ in range(5)]
    for time, voltage, current, rate, consumption in power_rows:
        time_list.append(time)
        voltage_list.append(voltage)
        current_list.append(current)
        rate_list.append(rate)
        consumption_list.append(consumption)

    power_line = (
        Line(init_opts=opts.InitOpts(
            bg_color="rgba(255, 250, 205, 0.2)",
            width="2400px",
            height="400px",
            theme=opts.global_options.ThemeType.MACARONS
        ))
            .add_xaxis(time_list)
            .add_yaxis("电压", voltage_list)
            .add_yaxis("电流", current_list)
            .add_yaxis("功率", rate_list)
            .add_yaxis("累计耗电量", consumption_list)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="耗电信息"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(item_width=60, item_height=30, selected_mode="multiple"),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True,
                    areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
        )
    )

    time_list, lines = [], []
    for key, content in groupby(temp_rows, key=lambda x: x[1]):
        if not time_list:
            values = []
            for time, _, value in content:
                time_list.append(time)
                values.append(value)
        else:
            values = [value for _, _, value in content]
        lines.append((layer_map[key], values))

    temp_line = Line(init_opts=opts.InitOpts(
            bg_color="rgba(255, 250, 205, 0.2)",
            width="2400px",
            height="400px",
            theme=opts.global_options.ThemeType.WHITE
        ))
    temp_line.add_xaxis(time_list)
    for (name, content), color in zip(lines, ['red', 'orange', 'yellow', 'green', 'blue', 'blank']):
        temp_line.add_yaxis(name, content, color=color)

    temp_line.set_global_opts(
        # title_opts=opts.TitleOpts(title="温度信息", pos_top="50%"),
        title_opts=opts.TitleOpts(title="温度信息"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross",),
        legend_opts=opts.LegendOpts(item_width=60, item_height=30, selected_mode="multiple"),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
    )

    time_list, yaw_list, pitch_list, roll_list, accx_list, accy_list, accz_list = [[] for _ in range(7)]
    for time, yaw, pitch, roll, acc_x , acc_y, acc_z in action_rows:
        time_list.append(time)
        yaw_list.append(yaw)
        pitch_list.append(pitch)
        roll_list.append(roll)
        accx_list.append(acc_x)
        accy_list.append(acc_y)
        accz_list.append(acc_z)

    action_line = (
        Line(init_opts=opts.InitOpts(
            bg_color="rgba(255, 250, 205, 0.2)",
            width="2400px",
            height="500px",
        ))
            .add_xaxis(time_list)
            .add_yaxis("yaw", yaw_list)
            .add_yaxis("pitch", pitch_list)
            .add_yaxis("roll", roll_list)
            .add_yaxis("acc_x", accx_list)
            .add_yaxis("acc_y", accy_list)
            .add_yaxis("acc_z", accz_list)
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="门的开关信息", pos_top="100%"),
            title_opts=opts.TitleOpts(title="门的开关信息"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(item_width=60, item_height=30, selected_mode="multiple"),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True,
                    areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
        )
    )

    # grid = (
    #     Grid(init_opts=opts.InitOpts(width="2600px", height="1200px"))
    #         .add(power_line, grid_opts=opts.GridOpts(pos_bottom="60%"))
    #         .add(temp_line, grid_opts=opts.GridOpts(pos_top="60%"))
    #         # .add(action_line, grid_opts=opts.GridOpts(pos_top="80%"))
    # )

    from pyecharts.charts import Page
    grid = Page(layout=Page.SimplePageLayout)
    grid.add(
        power_line,
        temp_line,
        action_line,
    )

    return HttpResponse(grid.render_embed())
