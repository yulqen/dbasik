import requests


def get_returns():
    """Returns a list of Return dicts"""
    response = requests.get("http://100.64.1.3:8000/api/returns/")
    if response:
        return response.json()
    else:
        print("Cannot reach API - is the server running?")


def get_items_for_return(rid, host="localhost"):
    """Get list of ReturnItem dicts for Return id of rid"""
    response = requests.get(f"http://{host}:8000/api/returnitems/")
    if response:
        out = []
        items = response.json()
        parent_url = f"http://{host}:8000/api/returns/"
        for i in items:
            if "".join([parent_url, str(rid), "/"]) == i["parent"]:
                out.append(i)
        return out
    else:
        print("Cannot reach API - is the server running?")


def print_key_values_from_return(rid, host="localhost"):
    ret_items = get_items_for_return(rid, host)
    for r in ret_items:
        kval = ""
        vval = ""
        dml = requests.get(r["datamapline"]).json()
        key = dml["key"]
        for k, v in r.items():
            if k in [
                "value_str",
                "value_int",
                "value_float",
                "value_date",
                "value_datetime",
                "value_phone",
            ]:
                kval = k
                vval = v
                break

        print(f"{key} - {kval}: {vval}")
