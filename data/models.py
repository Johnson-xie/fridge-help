from django.db import models


class Power(models.Model):
    time = models.DateTimeField(db_index=True)
    voltage = models.FloatField()
    current = models.FloatField()
    rate = models.FloatField()
    consumption = models.FloatField()

    class Meta:
        db_table = 'tbl_power'


class Door(models.Model):
    time = models.DateTimeField(db_index=True)
    yaw = models.FloatField()
    pitch = models.FloatField()
    roll = models.FloatField()
    acc_x = models.FloatField()
    acc_y = models.FloatField()
    acc_z = models.FloatField()

    class Meta:
        db_table = 'tbl_door'


class Temperature(models.Model):
    time = models.DateTimeField(db_index=True)
    code = models.CharField(max_length=128)
    value = models.FloatField()

    class Meta:
        db_table = 'tbl_temperature'
