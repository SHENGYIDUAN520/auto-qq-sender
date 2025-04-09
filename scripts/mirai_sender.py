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
logger = logging.getLogger('mirai-sender')

def send_message(target_qq, message, api_url, verify_key):
    """通过Mirai HTTP API发送QQ消息"""
    logger.info(f"尝试向{target_qq}发送消息")
    
    # TEST MODE - 模拟发送消息
    if api_url == "TEST":
        logger.info(f"测试模式：模拟向{target_qq}发送消息: '{message}'")
        return True
    
    # 去除URL末尾的斜杠，如果有的话
    api_url = api_url.rstrip('/')
    
    # 1. 获取会话
    session_url = f"{api_url}/auth"
    session_data = {
        "verifyKey": verify_key
    }
    
    try:
        # 获取会话
        session_response = requests.post(session_url, json=session_data)
        session_result = session_response.json()
        
        if session_result.get("code") != 0:
            logger.error(f"获取会话失败: {session_result}")
            return False
        
        session = session_result.get("session")
        logger.info(f"成功获取会话: {session}")
        
        # 2. 绑定会话
        bind_url = f"{api_url}/bind"
        bind_data = {
            "sessionKey": session,
            "qq": int(target_qq)  # 这里使用机器人自己的QQ号
        }
        
        bind_response = requests.post(bind_url, json=bind_data)
        bind_result = bind_response.json()
        
        if bind_result.get("code") != 0:
            logger.error(f"绑定会话失败: {bind_result}")
            return False
        
        logger.info("成功绑定会话")
        
        # 3. 发送消息
        send_url = f"{api_url}/sendFriendMessage"
        send_data = {
            "sessionKey": session,
            "target": int(target_qq),
            "messageChain": [
                {"type": "Plain", "text": message}
            ]
        }
        
        send_response = requests.post(send_url, json=send_data)
        send_result = send_response.json()
        
        if send_result.get("code") != 0:
            logger.error(f"发送消息失败: {send_result}")
            return False
        
        logger.info(f"成功发送消息到 {target_qq}")
        
        # 4. 释放会话
        release_url = f"{api_url}/release"
        release_data = {
            "sessionKey": session,
            "qq": int(target_qq)
        }
        
        requests.post(release_url, json=release_data)
        
        return True
    except Exception as e:
        logger.error(f"发送过程中出错: {str(e)}")
        return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='通过Mirai HTTP API发送QQ消息')
    parser.add_argument('--target', type=str, required=True, help='目标QQ号')
    parser.add_argument('--api-url', type=str, default="http://localhost:8080", help='Mirai HTTP API URL')
    parser.add_argument('--verify-key', type=str, required=True, help='Mirai HTTP API 验证密钥')
    parser.add_argument('--message', type=str, help='要发送的消息')
    parser.add_argument('--bot-qq', type=str, help='机器人自己的QQ号')
    parser.add_argument('--test', action='store_true', help='测试模式，不实际发送消息')
    args = parser.parse_args()
    
    # 如果没有提供消息，生成一个带随机代码的查寝消息
    if not args.message:
        random_code = random.randint(100, 999)
        args.message = f"查寝提醒：代码{random_code}，若请假请忽略此条消息，谢谢。"
    
    # 测试模式
    if args.test:
        args.api_url = "TEST"
    
    # 发送消息
    success = send_message(args.target, args.message, args.api_url, args.verify_key)
    
    if success:
        print(f"成功发送消息到 {args.target}")
    else:
        print(f"发送消息到 {args.target} 失败")

if __name__ == "__main__":
    main() 