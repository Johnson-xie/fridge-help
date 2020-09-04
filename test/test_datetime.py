import datetime
import os


d = datetime.date.today()
print(d)
# d2 = (d + datetime.timedelta(days=1))
# print(d, d2)
#
# print('%s' % d)
#
# d3 = datetime.datetime.strptime('2020-09-01')
# print(d3)


# print([file.split('.')[0] for file in os.listdir(r'E:\code\demo\data\templates') if file.endswith('html')])


t1 = datetime.datetime(2020, 9, 2, 10, 20, 30)
t2 = datetime.datetime(2020, 9, 2, 10, 20, 33)
delta = t2 - t1
print(delta.seconds)