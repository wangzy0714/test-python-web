# 做接口测试
import requests


class HttpApiTest:
    def test_get(self, url, data={}):
        res = requests.get(url, params=data)
        return res.text

    def test_post(self, url, data={}):
        res = requests.post(url, json=data)  # 这里用 json=data 代替 data=data
        return res.text

    def test_put(self, url, data={}):
        res = requests.put(url, data=data)
        return res.text

    def test_delete(self, url, data={}):
        res = requests.delete(url, params=data)
        return res.text


if __name__ == "__main__":
    httpapi = HttpApiTest()
    res = httpapi.test_get(
        "http://localhost:5000/user",
        data={"email": "123@qq.com", "password": "123"},
    )
    print(res)
