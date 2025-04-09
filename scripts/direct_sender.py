#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
import random
import logging
import json
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('direct-sender')

def send_qq_message(target_qq, message, server_url, token):
    """使用企业机器人API发送消息"""
    try:
        logger.info(f"尝试向{target_qq}发送消息")
        
        # 构建API请求
        api_url = f"{server_url}/send_message"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        payload = {
            "target": target_qq,
            "message": message,
            "type": "text",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 发送请求
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                logger.info(f"成功发送消息到 {target_qq}")
                return True
            else:
                logger.error(f"发送消息失败: {result.get('message')}")
                return False
        else:
            logger.error(f"API请求失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"发送过程中出错: {str(e)}")
        return False

def test_local_mode(target_qq, message):
    """本地模拟模式，不实际发送消息"""
    logger.info(f"[模拟模式] 向 {target_qq} 发送消息: {message}")
    print(f"[模拟发送] 发送至: {target_qq}")
    print(f"[模拟发送] 消息内容: {message}")
    print(f"[模拟发送] 发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[模拟发送] 状态: 成功")
    return True

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='发送QQ消息')
    parser.add_argument('--target', type=str, required=True, help='目标QQ号')
    parser.add_argument('--message', type=str, help='要发送的消息')
    parser.add_argument('--server', type=str, help='消息服务器URL')
    parser.add_argument('--token', type=str, help='API令牌')
    parser.add_argument('--local', action='store_true', help='仅本地模拟，不实际发送')
    args = parser.parse_args()
    
    # 如果没有提供消息，生成一个带随机代码的查寝消息
    if not args.message:
        random_code = random.randint(100, 999)
        args.message = f"查寝提醒：代码{random_code}，若请假请忽略此条消息，谢谢。"
    
    # 决定使用哪种发送模式
    if args.local:
        success = test_local_mode(args.target, args.message)
    else:
        if not args.server or not args.token:
            logger.error("非本地模式需要提供 server 和 token 参数")
            return
        success = send_qq_message(args.target, args.message, args.server, args.token)
    
    if success:
        print(f"成功发送消息到 {args.target}")
    else:
        print(f"发送消息到 {args.target} 失败")

if __name__ == "__main__":
    main() 