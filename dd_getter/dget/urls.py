from django.urls import path, include
import dget.views

urlpatterns = [
    path("", dget.views.index, name="index"),
    path("upda/", dget.views.upd_a, name="upda"),
    path("updp/", dget.views.upd_p, name="updp"),
    path("updc/", dget.views.upd_c, name="updc"),
    path("updb/", dget.views.upd_b, name="updb"),
    path("save/", dget.views.save_upd, name="save"),
    path("ov/", dget.views.overview, name="overview"),
    path("empr/", dget.views.missing_by_prod, name="empty by product"),
    path("emall/", dget.views.missingall, name="empty completely"),
    path("stock/", dget.views.avaliable, name="stock"),
    path("debug/", dget.views.debug_db_record, name="debug"),
    path("json/", dget.views.get_latest_json, name="json"),
    # path("db/", dget.views.db, name="db"),
]
