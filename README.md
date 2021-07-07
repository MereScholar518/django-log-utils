# django-log-utils

## 1.说明
```text
该工具用于记录django web项目中的请求日志和异常日志
```

## 2.使用示例

### 记录请求日志
```text
项目目录结构
my_web_service
├── db.sqlite3
├── log
│   └── request_log_2021-07-07.log
├── main
│   ├── __init__.py
│   ├── __pycache__
│   │   └── __init__.cpython-36.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── utils
│   │   ├── LogUtils.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── LogUtils.cpython-36.pyc
│   │       └── __init__.cpython-36.pyc
│   └── views.py
├── manage.py
└── my_web_service
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   ├── settings.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── wsgi.cpython-36.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py



编辑settings.py

MIDDLEWARE = [
    'main.utils.LogUtils.AccessLogMiddleware',
     ......
]

查看request_log_2021-07-07.log，效果如下：
DEBUG--2021-07-07 03:32:23--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.0099639892578125
--------------------------------------------------
DEBUG--2021-07-07 03:32:41--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.0005769729614257812
--------------------------------------------------


```

### 记录异常日志
```text
添加视图
from django.http import JsonResponse
from django.views import View
from main.utils.LogUtils import record_request_log


class Test(View):

    def get(self, request):
        record_request_log("ERROR", "你好呀！")
        return JsonResponse(status=200, data={"response": "Hello World!"})


查看request_log_2021-07-07.log，效果如下
DEBUG--2021-07-07 03:32:23--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.0099639892578125
--------------------------------------------------
DEBUG--2021-07-07 03:32:41--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.0005769729614257812
--------------------------------------------------
ERROR--你好呀！
--------------------------------------------------
DEBUG--2021-07-07 03:37:15--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.005735874176025391
--------------------------------------------------
ERROR--你好呀！
--------------------------------------------------
DEBUG--2021-07-07 03:37:16--http://127.0.0.1:8000/test/--未传递--GET--127.0.0.1--Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36--{}--{'response': 'Hello World!'}--0.0007460117340087891
--------------------------------------------------

```

