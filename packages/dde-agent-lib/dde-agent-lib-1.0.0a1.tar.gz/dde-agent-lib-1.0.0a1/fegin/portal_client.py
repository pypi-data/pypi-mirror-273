import json

import requests


class PortalClient:

    def __init__(self, logger, portal_address, system_config):
        self.logger = logger
        self.portal_address = portal_address
        self.chatdetail_url = system_config['feign']['portal']['chatdetail_url']
        self.savechat_url = system_config['feign']['portal']['savechat_url']
        self.exception_process_url = system_config['feign']['portal']['exception_process_url']

    def get_chat_detail(self, sessionId: str):
        """
        获取历史聊天信息
        """
        url = f"{self.portal_address}{self.chatdetail_url}"
        with requests.Session() as session:
            response = session.get(url, params={"sessionId": sessionId})
            chat_detail = response.json()
            return chat_detail

    def save_chat(self, data: dict):
        """
        portal存储聊天返回
        """
        url = f"{self.portal_address}{self.savechat_url}"
        hearders = {
            "Content-Type": "application/json"
        }
        with requests.Session() as session:
            response = session.post(url, data=json.dumps(data), headers=hearders)
            save_chat_response = response.json()
            self.logger.info(f"回调portal后端的地址为[{url}]，回调数据为[{json.dumps(data)}]")
            return save_chat_response

    def exception_process(self, data: dict):
        """
        portal异常处理接口
        """
        # portal_address = "http://10.101.120.2:8065"
        url = f"{self.portal_address}{self.exception_process_url}"
        hearders = {
            "Content-Type": "application/json"
        }
        with requests.Session() as session:
            response = session.post(url, data=json.dumps(data), headers=hearders)
            exception_process_response = response.json()
            return exception_process_response
