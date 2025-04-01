#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('qq-sender')

# 从环境变量获取配置
API_URL = os.environ.get('QQ_API_URL')  # go-cqhttp的API地址
API_TOKEN = os.environ.get('QQ_API_TOKEN')  # API访问令牌
QQ_TARGETS = os.environ.get('QQ_TARGETS')  # 目标QQ号，用逗号分隔

# 检查时间是否需要发送消息（比如只在晚上查寝）
def should_send_now():
    now = datetime.now()
    # 例如：晚上10点到11点之间发送查寝消息
    if 22 <= now.hour < 23:
        return True
    return False

# 发送QQ消息函数
def send_qq_message(target_qq, message):
    if not API_URL:
        logger.error("未设置QQ_API_URL环境变量")
        return False
        
    headers = {
        "Content-Type": "application/json"
    }
    
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    
    data = {
        "user_id": int(target_qq),
        "message": message
    }
    
    try:
        # 发送私聊消息API
        response = requests.post(
            f"{API_URL}/send_private_msg",
            headers=headers,
            data=json.dumps(data)
        )
        
        result = response.json()
        if result.get("status") == "ok":
            logger.info(f"成功发送消息到 {target_qq}")
            return True
        else:
            logger.error(f"发送失败: {result}")
            return False
    except Exception as e:
        logger.error(f"发送过程中出错: {str(e)}")
        return False

def main():
    if not should_send_now():
        logger.info("当前时间不需要发送查寝消息")
        return
    
    if not QQ_TARGETS:
        logger.error("未设置QQ_TARGETS环境变量")
        return
    
    # 查寝消息内容
    message = "查寝提醒：请回复「在」确认你已在宿舍。10分钟内未回复将被记为缺勤。"
    
    # 给每个目标QQ发送消息
    targets = QQ_TARGETS.split(',')
    for target in targets:
        target = target.strip()
        if target:
            send_qq_message(target, message)
            # 添加延迟避免频率限制
            time.sleep(1)

if __name__ == "__main__":
    main() 