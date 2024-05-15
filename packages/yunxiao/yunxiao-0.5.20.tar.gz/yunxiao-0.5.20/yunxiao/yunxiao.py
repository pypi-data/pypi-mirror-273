import logging
import time
import requests


def timestamp():
    return int(time.time() * 1000)


class YunXiao:

    def __init__(self, user, pwd, campus: tuple = ()):
        self.host = 'clouds.xiaogj.com'
        self.session = requests.Session()
        self.user, self.pwd = user, pwd
        self.headers = self.renew_auth()
        self.campus = list(campus)

    def renew_auth(self):
        """
        刷新 token.tmp 配置中存储的 token
        """
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                   "Origin": F"https://{self.host}",
                   "Yunxiao-Version": "3.51"}
        self.session.headers.update(headers)

        applogin = self.session.post(
            url=f"https://{self.host}/api/cs-crm/teacher/loginByPhonePwd",
            json={"_t_": timestamp(), "password": self.pwd, "phone": self.user, "userType": 1}
        ).json()["data"]["token"]

        headers["x3-authentication"] = self.session.get(
            url=f"https://{self.host}/api/cs-crm/teacher/businessLogin",
            headers={"x3-authentication": applogin},
            params={"_t_": timestamp()}
        ).json()["data"]["token"]

        # 刷新 cookie

        weblogin = self.session.post(
            url="https://clouds.xiaogj.com/api/ua/login/password",
            params={"productCode": 1, "terminalType": 2, "userType": 1, "channel": "undefined"},
            json={"_t_": timestamp(), "clientId": "x3_prd", "password": self.pwd, "username": self.user,
                  "redirectUri": f"https://{self.host}/web/teacher/#/home/0",
                  "errUri": f"https://{self.host}/web/simple/#/login-error"},
            allow_redirects=False
        )

        weboauth2 = self.session.get(url=weblogin.json()["data"], allow_redirects=False)
        webcode = self.session.get(url=weboauth2.headers["location"], allow_redirects=False)
        webtoken = self.session.get(url=webcode.headers["location"], allow_redirects=False)

        headers["Cookie"] = (f'UASESSIONID={weblogin.cookies.get("UASESSIONID")}; '
                             f'SCSESSIONID={webtoken.cookies.get("SCSESSIONID")}')
        logging.info("登录成功")
        return headers

    def request(self, **kwargs) -> dict:
        response = self.session.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                        params=kwargs.get("params"), headers=self.headers)

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        r_json = response.json()

        if r_json.get("code") == 401:
            logging.error(r_json.get("msg", '未知问题，尝试重新登录。'))
            self.headers = self.renew_auth()
            response = requests.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                        params=kwargs.get("params"), headers=self.headers)

        return response.json()

    def pages_looper(self, endpoint, payload, schemas):
        response = schemas()  # 结果列表
        response.page.pageSize = payload.page.pageSize
        while payload.page.pageNum <= response.page.totalPage:
            res = self.request(method="post", url=endpoint, json=payload.model_dump())
            try:
                new = schemas(**res)
                response.data.extend(new.data)
                response.page = new.page

                logging.info(
                    f"\033[32m size \033[36m{payload.page.pageSize}"
                    f"\033[32m page \033[36m{response.page.pageNum}/{response.page.totalPage}"
                    f"\033[32m count \033[36m{response.page.pageNum * payload.page.pageSize}/{response.page.totalCount}"
                    f"\033[0m\t{endpoint}"
                )  # 汇报数量

                payload.page.pageNum += 1  # 翻页
            except TypeError:
                logging.error(res)
        response.page.pageSize = payload.page.pageSize
        return response

    # 查询校区（APP接口）
    def campus_query(self) -> list:
        """
        查询全部校区
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/campus/list?type=2"
        )["data"]

    # 查询招生来源
    def comefroms_query(self):
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/customField/get",
            params={"_t_": timestamp(), "customFieldId": "26118419"}
        )["data"]["selectItemList"]
