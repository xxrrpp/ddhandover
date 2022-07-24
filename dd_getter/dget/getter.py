# -*- coding: utf-8 -*-
"""
r
"""
import time
import dget.cloudscraper as cloudscraper

from bs4 import BeautifulSoup
from collections import OrderedDict
import pickle
import time
import copy

url = ""
arg = "product"
per = "product"
col = "product"
bol = "product"


class CityStat:
    def __init__(self, name, distr, av=None):
        self.name = name
        dr = sorted(distr, key=lambda x: x.split(" ")[1])
        # for i, v in enumerate(distr):
        self.distr = dr  # sorted(
        self.avaliable = OrderedDict() if av is None else av

    def check(self):
        rem = []
        upd = []
        for k, v in self.avaliable.items():
            if k not in self.distr:
                upd.append(v)
                rem.append(k)
        for k in rem:
            self.avaliable.pop(k)
        for v in upd:
            if "весь город" not in self.avaliable.keys():
                self.avaliable["весь город"] = copy.deepcopy(v)
            else:
                self.avaliable["весь город"].extend(v)
        return self

    def get_empty(self):
        set1 = set(self.distr)
        set2 = set(self.avaliable.keys())
        r = sorted(list(set1 ^ set2))
        return "\n".join(r)

    def format_districts(self):
        self.name = self.name.upper()
        for i, v in enumerate(self.distr):
            self.distr[i] = change(v)

        pl = [[k, v] for k, v in self.avaliable.items()]
        for i, v in enumerate(pl):
            pl[i][0] = change(v[0])

        self.avaliable = OrderedDict(pl)

    def to_dict(self):
        res = OrderedDict()
        res[self.name] = OrderedDict()
        res[self.name]["distr"] = copy.deepcopy(self.distr)
        res[self.name]["avaliable"] = copy.deepcopy(self.avaliable)
        return res

    @staticmethod
    def from_dict(d):
        ct = []
        for k, v in d.items():
            # print(k)
            name = k
            distr = v["distr"]
            av = v["avaliable"]
            ct.append(CityStat(name, distr, av))
            # ct.distr = d[name]["distr"]
        return ct[0]

    def __repr__(self):
        if self.name.lower() in "Москва".lower():
            name = "мск"
        if self.name.lower() in "Санкт-Петербург".lower():
            name = "спб"
        if self.name.lower() in "Красногорск".lower():
            name = "кгк"
        st = " + {}:".format(name)
        return "{} {}/{}".format(
            st,
            str(len(self.avaliable)).rjust(3, " "),
            str(len(self.distr)).ljust(3, " "),
        )

    def __str__(self):
        return repr(self) + "\n   "


def change(y):
    x = y
    x = x.replace("метро", "-м-")
    x = x.replace("монорельс", "мрc")
    x = x.replace("МЦК", "мцк")
    x = x.replace("район", "р-н")
    x = x.replace("проспект", "пр")
    x = x.replace("Проспект", "пр")
    x = x.replace("Улица", "ул")
    x = x.replace("шоссе", "ш")
    x = x.replace("площадь", "пл")
    x = x.replace("Площадь", "пл")
    x = x.replace("бульвар", "бл")
    x = x.replace("Бульвар", "бл")
    x = x.replace("имени", "им")
    x = x.replace("институт", "инст")
    x = x.replace("Невского", "невс")
    if x.startswith(" "):
        x = x[1:]
    return x.lower()


def bypass_get(url):
    scraper = cloudscraper.create_scraper(delay=25)
    data = scraper.get(url).text
    time.sleep(10)
    data = scraper.get(url)
    return data


def get_distr_templates(loc, cities):

    locations = [l.strip() for l in loc][1:]
    cty = []
    dst = []
    rem = None

    for c, v in enumerate(cities):
        if rem is None:
            rem = locations[:]
        st = rem.index(v)
        en = 0
        if c + 1 < len(cities):
            en = rem.index(cities[c + 1])
            loc = rem[st]
            addr = rem[st + 1 : en]
            rem = rem[en:]
        else:
            loc = rem[st]
            addr = rem[st + 1 :]

        cty.append(loc)
        dst.append(addr)

    return [CityStat(t[0], t[1]) for t in zip(cty, dst)]


def get_items(store):
    st = [l.strip() for l in store]
    st[0] = st[0].split("По предзаказу")[1][5:]
    st = "*".join(st)

    def find_block(val, sep="/"):
        s = val.find(sep)
        e = val.find(sep, s + 1)
        if e != -1:
            end = val[:e].rindex("*")
            res = val[:end]
            rem = val[end + 1 :]
            return res, rem
        else:
            return val, None

    rem = st
    while rem is not None:
        res, rem = find_block(rem)
        yield res


def parse_product_page(pname, page):
    cities = ["Москва", "Санкт-Петербург", "Красногорск"]
    locs = "Любая локация"
    store = "Любой тип"
    end = "Оформить предзаказ"
    buy = "Купить"

    bs = BeautifulSoup(page, "html.parser")
    text = "\n".join(
        [l.strip() for l in bs.get_text().splitlines() if len(l.strip()) > 1]
    )
    storefront = text.split(locs)[1].split(store)[1].split(end)[0].split(buy)
    districts = text.split(locs)[1].split(store)[0].splitlines()
    ct = get_distr_templates(districts, cities)

    for item in get_items(storefront):
        i = item.split("/")
        city = i[0]
        spl = i[1].find("\n")
        distr = OrderedDict()
        distr[i[1][1:spl]] = [
            [vv for vv in v.splitlines()[:-2] if vv and vv.lower() not in "москва"]
            for v in i[1][spl:].split("*")
        ]

        for k, v in distr.items():
            for i, p in enumerate(distr[k]):
                if "москва" in str(p).lower():
                    distr[k][i].pop()

        for ci, cv in enumerate(ct):
            if ct[ci].name not in city:
                continue
            for k in distr:
                ct[ci].avaliable[k] = []
                for i in distr[k]:
                    iv = [v.replace(" г", "") for v in i]
                    if len(iv) == 1:
                        iv.append("na")
                    w = [v for v in iv if v.endswith("0")]
                    if len(w) == 1:
                        w = w[0]
                    t = [(v, w) for v in iv if not v.endswith("0")]
                    ct[ci].avaliable[k].extend(t)
    return ct


def recieve_products(names=None):
    if names is None:
        names = ["|A|", "|P|", "|C|", "|B|"]
    urls = {"|A|": arg, "|P|": per, "|C|": col, "|B|": bol}
    products = OrderedDict()

    for i, n in enumerate(names):
        print("geting ", n, time.ctime(time.time()))
        products[n] = parse_product_page(n, bypass_get(urls[n]).text)

    for k in products:
        for i, ct in enumerate(products[k]):
            products[k][i].format_districts()
    return products


def stat_string(prod):

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
        e = set(ema) & set(emp) & set(emc) & set(emb)
        ee = []
        ee.extend(ema)
        ee.extend(emp)
        ee.extend(emc)
        ee.extend(emb)
        ee = set(ee)
        empty[v.name] = sorted(list(e))

    res_empty = copy.deepcopy(prod)
    res_empty["|+|"] = copy.deepcopy(ma)
    for ii, vv in enumerate(res_empty["|+|"]):
        res_empty["|+|"][ii].avaliable = OrderedDict(
            zip(res_empty["|+|"][ii].distr, res_empty["|+|"][ii].distr)
        )
    for k, v in empty.items():
        for ii, vv in enumerate(res_empty["|+|"]):

            nm = vv.name.lower()
            kk = k.lower()
            if nm in kk:
                for d in v:
                    res_empty["|+|"][ii].avaliable.pop(d)
                    # print(res_empty["|+|"][ii].avaliable[d])
    result = "\n"
    for n, v in res_empty.items():
        if n in "|+|":
            result = result[:-4] + "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"
            result += "+" + n[1] + "+"
        else:
            result += "-" + n[1] + "-"
        result += "".join([str(vv) for vv in v]) + "\n"
    return result


# def recieve():
#     prod = recieve_products()
#     empty = "\n".join([c.name + "\n\n" + c.get_empty() + "\n" for c in prod["|A|"]])
#     r = "\n".join([time.ctime(time.time()), stat_string(prod), empty])
#     return r


# if __name__ == "__main__":
#     print(recieve_json())
# return stat_string(recieve_products())
