import datetime
import json
import os
import time

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AccessLogMiddleware(MiddlewareMixin):
    """
    访问记录中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        request.META["HTTP_START_TIME"] = time.time()

    def process_response(self, request, response):
        if 'admin' not in request.path and 'favicon.ico' not in request.path and 'notice' not in request.path:
            self.insert_access_log_util(request, response)
        return response

    @staticmethod
    def get_request_dict(request):
        """
        获取请求参数字典
        :return:
        """
        request_data = dict()
        try:
            request_data.update(json.loads(request.body))
        except:
            request_data.update(request.GET.dict())
            request_data.update(request.POST.dict())
        return request_data

    def insert_access_log_util(self, request, response):
        """
        创建访问记录工具
        :return:
        """

        meta = request.META
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 请求的完整地址
        request_path = request.get_host() if ':' in request.get_host() else request.get_host() + ':' + request.META.get(
            'SERVER_PORT', '')  # 服务端ip
        request_path = request.scheme + "://" + request_path + request.path
        # 本次请求的uuid
        request_uuid = meta.get("HTTP_X_REQUEST_TRACE_ID", "未传递")
        # 客户端的ip
        client_ip = meta.get('HTTP_X_FORWARDED_FOR') if meta.get('HTTP_X_FORWARDED_FOR') else meta.get('REMOTE_ADDR')
        # 客户端的user-agent
        user_agent = meta.get("HTTP_USER_AGENT")
        # method
        method = request.method
        # 耗时/秒
        time_consuming = time.time() - request.META["HTTP_START_TIME"]
        # 请求数据
        req_data = str(self.get_request_dict(request))
        # 返回数据
        rsp_data = str(json.loads(response.content) if isinstance(response, JsonResponse) else "")

        log_content = f"{date_time}--{request_path}--{request_uuid}--" \
                      f"{method}--{client_ip}--{user_agent}--" \
                      f"{req_data}--{rsp_data}--{time_consuming}"
        record_request_log("DEBUG", log_content)


def record_request_log(log_level, log_content):
    """
    记录日志
    :return:
    """
    today_day = datetime.datetime.now().strftime("%Y-%m-%d")

    # 压缩日志
    base_path = f"{settings.BASE_DIR}/log/"
    file_list = os.listdir(base_path)
    for i in file_list:
        if "log" in i and today_day not in i and "gz" not in i:
            os.popen(f"gzip -N -9 {base_path}{i}")

    with open(f"{settings.BASE_DIR}/log/request_log_{today_day}.log", "a+", encoding="utf-8") as f:
        f.write(log_level + "--" + log_content + "\n" + "-" * 50 + "\n")
