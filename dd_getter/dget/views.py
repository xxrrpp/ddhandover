from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import dget.getter as getter
from dget.models import Greeting, InfoDump
from dget.info import (
    fetch_to_db,
    from_db_to_prod,
    get_overview,
    get_empty_prod,
    get_empty_all,
    get_avaliable,
)
from collections import OrderedDict
import copy
import json


def index(request):
    return HttpResponse("hi there")
    # return render(request, "index.html")


def process_upd(n):
    p = fetch_to_db(name=n)
    d = OrderedDict()
    for k, v in p.items():
        d[k] = [vv.to_dict() for vv in v]
    dump = d
    # dump = json.dumps(d, indent=2, ensure_ascii=False)
    return dump


def upd_a(request):
    n = "|A|"
    # request.session["prod"]
    p = copy.deepcopy(process_upd(n))
    request.session["prod"] = p
    o = len(p.values())
    return HttpResponse("{}:{} >> session".format(n, o))
    # prod = fetch_to_db(name=n)


def upd_p(request):
    n = "|P|"
    d = OrderedDict()
    # a = json.loads(request.session["prod"])
    a = request.session["prod"]
    # print(a)
    for k, v in a.items():
        d[k] = v
    p = copy.deepcopy(process_upd(n))
    for k, v in p.items():
        d[k] = v
    request.session["prod"] = d
    o = len(p.values())
    return HttpResponse("{}:{} >> session".format(n, o))


def upd_c(request):
    n = "|C|"
    d = OrderedDict()
    # a = json.loads(request.session["prod"])
    a = request.session["prod"]
    # print(a)
    for k, v in a.items():
        d[k] = v
    p = copy.deepcopy(process_upd(n))
    for k, v in p.items():
        d[k] = v
    request.session["prod"] = d
    o = len(p.values())
    return HttpResponse("{}:{} >> session".format(n, o))


def upd_b(request):
    n = "|B|"
    d = OrderedDict()
    # a = json.loads(request.session["prod"])
    a = request.session["prod"]
    # print(a)
    for k, v in a.items():
        d[k] = v
    p = copy.deepcopy(process_upd(n))
    for k, v in p.items():
        d[k] = v
    request.session["prod"] = d
    o = len(p.values())
    return HttpResponse("{}:{} >> session".format(n, o))


def save_upd(request):
    prod = OrderedDict()
    for k, v in request.session["prod"].items():
        prod[k] = []
        for vv in v:
            prod[k].append(getter.CityStat.from_dict(vv))
    dump_info = InfoDump.create(prod)
    dump_info.save()
    print("all ->> saved to DB")
    request.session.flush()
    st = [str(k) + str([str(vv) for vv in v]) for k, v in prod.items()]
    return HttpResponse("\n".join(st), content_type="text/plain; charset=utf-8")
    # return HttpResponse(
    #     prod["|B|"][2].avaliable.values(), content_type="text/plain; charset=utf-8"
    # )


def overview(request):
    db_info = InfoDump.objects.filter().latest("id")
    prod = from_db_to_prod(db_info.data)
    c = "text/plain; charset=utf-8"
    # v = str(db_info.id) + get_overview(prod, str(db_info.when)[5:-13])
    v = str(get_overview(prod, str(db_info.when)[5:-13]))
    return HttpResponse(v, content_type=c)


def missing_by_prod(request):
    db_info = InfoDump.objects.filter().latest("id")
    prod = from_db_to_prod(db_info.data)
    c = "text/plain; charset=utf-8"
    v = get_empty_prod(prod, str(db_info.when)[5:-13])
    return HttpResponse(v, content_type=c)


def missingall(request):
    db_info = InfoDump.objects.filter().latest("id")
    prod = from_db_to_prod(db_info.data)
    c = "text/plain; charset=utf-8"
    v = get_empty_all(prod, str(db_info.when)[5:-13])
    return HttpResponse(v, content_type=c)


def avaliable(request):
    db_info = InfoDump.objects.filter().latest("id")
    prod = from_db_to_prod(db_info.data)
    c = "text/plain; charset=utf-8"
    v = get_avaliable(prod, str(db_info.when)[5:-13])
    return HttpResponse(v, content_type=c)


def debug_db_record(request):
    db_info = InfoDump.objects.filter().latest("id")
    prod = from_db_to_prod(db_info.data)
    res = ""
    res += "id: {}   time: {}\n".format(db_info.id, db_info.when)
    for k, v in prod.items():
        res += "\n" + k + "\n"
        for cty in v:
            res += cty.name + "\n"
            for dis in cty.distr:
                res += dis
                if dis in cty.avaliable.keys():
                    res += "  " + str(cty.avaliable[dis])
                res += "\n"
            res += "\n"
        res += "\n"
    c = "text/plain; charset=utf-8"
    return HttpResponse(res, content_type=c)


def get_latest_json(request):
    db_info = InfoDump.objects.filter().latest("id")
    c = "text/plain; charset=utf-8"
    return HttpResponse(db_info.data, content_type=c)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
