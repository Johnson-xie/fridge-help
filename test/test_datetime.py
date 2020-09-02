import datetime

d = datetime.date.today()
d2 = (d + datetime.timedelta(days=1))
print(d, d2)

print('%s' % d)

d3 = datetime.datetime.strptime('2020-09-01', '%Y-%m-%d')
print(d3)
