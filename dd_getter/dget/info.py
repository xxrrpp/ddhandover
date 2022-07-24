import dget.getter as gt
from dget.models import InfoDump
from collections import OrderedDict
import json
import time


def fetch_to_db(name):
    print(name, "fetching update from urls ", time.ctime(time.time()))
    # prod = gt.recieve_products(local=True)
    prod = gt.recieve_products(names=[name])
    print(name, "done update from urls ", time.ctime(time.time()))
    return prod


def from_db_to_prod(js):
    dct = json.loads(js)

    print("json loads res")
    prod = OrderedDict()
    for k, v in dct.items():
        prod[k] = []
        for vv in v:
            ct = gt.CityStat.from_dict(vv)
            ct.check()
            prod[k].append(ct)
    return prod


def get_overview(prod, timestamp):
    over = "——————————————————\n"
    over += "общее состояние   \n"
    over += "——————————————————\n"
    over += "" + timestamp + "\n"
    over += "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⏷\n"
    over += gt.stat_string(prod)
    return over


def get_empty_prod(prod, timestamp):
    res = "————————————————————————\n"
    res += "пустые: по типам позиций\n"
    res += "————————————————————————\n"
    res += "upd:-----" + timestamp + "\n"
    res += "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⏷\n"

    for k, v in prod.items():
        res += "\n•••" + k[1] + "•••\n\n"
        for cty in v:
            n = cty.name
            em = cty.get_empty()
            res += n + "\n"
            res += em + ".\n\n"
    return res


def get_empty_all(prod, timestamp):
    res_empty = "————————————————————————\n"
    res_empty += "пустые: ни одной позиции\n"
    res_empty += "————————————————————————\n"
    res_empty += "upd:-----" + timestamp + "\n"
    res_empty += "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⏷\n"

    ma = prod["|A|"]
    mp = prod["|P|"]
    mc = prod["|C|"]
    mb = prod["|B|"]

    empty = {}
    for i, v in enumerate(ma):
        ema = ma[i].get_empty().splitlines()
        emp = mp[i].get_empty().splitlines()
        emc = mc[i].get_empty().splitlines()
        emb = mb[i].get_empty().splitlines()
        # ee = {}
        # all = []
        # all.extend(ema)
        # all.extend
        e = set(ema) & set(emp) & set(emc) & set(emb)
        empty[v.name] = sorted(list(e))

    for k, v in empty.items():
        # empty = "\n".join([c.name + ":\n" + c.get_empty()+".\n" for c in prod[k]])
        res_empty += "\n×××" + k + "×××\n"
        res_empty += "\n".join(v) + ".\n"
    return res_empty


def get_avaliable(prod, timestamp):
    mlen = sum(
        sum(
            [[[len(vv) for vv in p.avaliable] for p in v] for k, v in prod.items()], []
        ),
        [],
    )
    mlen = max(mlen)
    store = "———————————————————————\n"
    store += "общее состояние позиций\n"
    store += "———————————————————————\n"
    store += "upd:----" + timestamp + "\n"
    store += "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⏷\n"

    for k, v in prod.items():
        store += "\n•••" + k[1] + "•••\n\n"
        for p in v:
            n = p.name
            store += n + "\n"
            for i, q in p.avaliable.items():
                qq = []
                av = i.ljust(mlen + 1, "᛫")
                for ii, vv in enumerate(q):
                    x = vv[0]
                    y = vv[1]

                    xy = "⁞ {} ⁞{}⬝{}⁞".format(y[:-1], x[0], x[1])
                    if ii >= 1:
                        xy = "\n" + "".ljust(mlen + 1, " ") + xy
                    # xy = "|| {} : {}{} ||".format(y[:-1],x[0], x[1])
                    qq.append(xy)
                if qq:
                    av += "".join(qq)
                store += av + "\n"

            store += "\n"
    return store


# if __name__ == "__main__":
#     # fetch_to_db()
