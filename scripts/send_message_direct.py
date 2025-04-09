#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
import random
import logging
import json
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('qq-direct-sender')

def send_message(target_qq, message, api_url):
    """直接通过HTTP API发送QQ消息"""
    logger.info(f"尝试向{target_qq}发送消息")
    
    # 去除URL末尾的斜杠，如果有的话
    api_url = api_url.rstrip('/')
    
    # 构建完整的API URL
    url = f"{api_url}/send_private_msg"
    
    # 准备请求参数
    params = {
        "user_id": int(target_qq),
        "message": message
    }
    
    try:
        # 发送GET请求
        logger.info(f"发送请求到: {url} 参数: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应内容: {response.text[:200]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") == "ok" or result.get("retcode") == 0:
                    logger.info(f"成功发送消息到 {target_qq}")
                    return True
                else:
                    logger.error(f"API返回错误: {result}")
            except:
                logger.warning("无法解析JSON响应，但状态码为200，可能已发送成功")
                return True
    except Exception as e:
        logger.error(f"发送失败: {str(e)}")
    
    return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='直接通过HTTP API发送QQ消息')
    parser.add_argument('--target', type=str, required=True, help='目标QQ号')
    parser.add_argument('--api-url', type=str, required=True, help='API URL，例如http://1064ju811jp02.vicp.fun:13701')
    parser.add_argument('--message', type=str, help='要发送的消息')
    args = parser.parse_args()
    
    # 如果没有提供消息，生成一个带随机代码的查寝消息
    if not args.message:
        random_code = random.randint(100, 999)
        args.message = f"查寝提醒：代码{random_code}，若请假请忽略此条消息，谢谢。"
    
    # 发送消息
    success = send_message(args.target, args.message, args.api_url)
    
    if success:
        print(f"成功发送消息到 {args.target}")
    else:
        print(f"发送消息到 {args.target} 失败")

if __name__ == "__main__":
    main() 