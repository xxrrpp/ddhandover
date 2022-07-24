from django.db import models
from collections import OrderedDict
import json


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class InfoDump(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    data = models.JSONField(null=True)

    @classmethod
    def create(cls, prod):
        d = OrderedDict()
        for k, v in prod.items():
            d[k] = [vv.to_dict() for vv in v]

        dump = cls(data=json.dumps(d, indent=2, ensure_ascii=False))
        return dump
