import time
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Sites_all, Siterecs_hfp_fqhc

table_dict = {
    "sitecodes_samhsa_ftloc": Sitecodes_samhsa_ftloc,
    "siterecs_samhsa_ftloc": Siterecs_samhsa_ftloc,
    "siterecs_hfp_fqhc": Siterecs_hfp_fqhc,
    "siterecs_samhsa_otp": Siterecs_samhsa_otp ,
    "siterecs_dbhids_tad": Siterecs_dbhids_tad,
    "siterecs_other_srcs" : Siterecs_other_srcs ,
    "sites_all" : Sites_all,
}

cachedTables = {
    # "table_name": {"data": ..., "cacheTime": time_table_was_cached}
}
def fetchCachedIfRecent(table_name, ttl=120):
    if table_name not in cachedTables or not (time.time() - cachedTables[table_name]["cacheTime"]) < ttl:
        cachedTables[table_name] = {"data": table_dict[table_name].objects.all(), "cacheTime": time.time()}
    return cachedTables[table_name]["data"]