from yunxiao import YunXiao
import time


def query_report(auth: YunXiao, startDate: str, endDate: str) -> list:
    """
    分校区列出指定日期的费用数据。
    :param auth:
    :param startDate:
    :param endDate:
    :return:
    """
    data = auth.request(
        method="post",
        url=f"https://{auth.host}/api/cs-report/report/findDataReportList",
        json={
            "campusIds": auth.campus,
            "startDate": startDate,
            "endDate": endDate,
            "orderByCampus": 1,
            "_t_": int(time.time() * 1000)
        }
    ).get("data").get("dataReportVos")
    return data
