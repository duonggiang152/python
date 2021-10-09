"""
Yêu cầu thêm modul request
"""
import requests
import sys
def duLieuTrongNuoc():
    """
        Lấy data covid 19 trong nước
        :return: dictionary
    """
    response = requests.get("https://static.pipezero.com/covid/data.json")
    return response.json()["total"]["internal"]
# sys.modules[__name__] = duLieuTrongNuoc