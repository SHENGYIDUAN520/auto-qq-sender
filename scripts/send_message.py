#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
import logging
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import argparse  # 添加命令行参数支持

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

# 检查时间是否需要发送消息
def should_send_now():
    # 检查是否是手动触发的工作流
    if os.environ.get('WORKFLOW_TRIGGER') == 'manual':
        return True
        
    now = datetime.now()
    # 晚上22:40发送查寝消息
    if now.hour == 22 and now.minute == 40:
        return True
    return False

# 发送QQ消息函数
def send_qq_message(target_qq, message):
    if not API_URL:
        logger.error("未设置QQ_API_URL环境变量")
        return False
        
    # 去除URL末尾的斜杠，如果有的话
    api_base_url = API_URL.rstrip('/')
    
    # 尝试请求API版本信息，检查连接是否正常
    try:
        version_url = f"{api_base_url}/get_version_info"
        logger.info(f"尝试获取API版本信息: {version_url}")
        version_response = requests.get(version_url, timeout=10)
        logger.info(f"API版本响应状态码: {version_response.status_code}")
        logger.info(f"API版本响应内容: {version_response.text[:200]}...")
    except Exception as e:
        logger.error(f"获取API版本信息失败: {str(e)}")
        
    headers = {
        "Content-Type": "application/json"
    }
    
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    
    # 使用不同格式的数据发送尝试
    
    # 1. 标准JSON格式
    json_data = {
        "user_id": int(target_qq),
        "message": message
    }
    
    # 2. URL查询参数格式
    params_data = {
        "user_id": target_qq,
        "message": message
    }

    # 多个可能的API路径
    api_paths = [
        "/send_private_msg",
        "/send_msg",
    ]
    
    # 尝试不同的请求方法
    for api_path in api_paths:
        # 尝试POST JSON
        try:
            full_url = f"{api_base_url}{api_path}"
            logger.info(f"尝试使用POST JSON发送消息到 {target_qq}, API地址: {full_url}")
            
            response = requests.post(
                full_url,
                headers=headers,
                json=json_data,  # 使用json参数而不是data+json.dumps
                timeout=10
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            logger.info(f"API响应内容: {response.text[:200]}...")
            
            # 检查响应
            if response.status_code == 200:
                try:
                    result = response.json()
                    if (result.get("status") == "ok" or 
                        result.get("retcode") == 0 or 
                        result.get("data", {}).get("message_id", None) is not None):
                        logger.info(f"成功发送消息到 {target_qq}")
                        return True
                except:
                    if "success" in response.text.lower():
                        logger.info(f"可能成功发送消息到 {target_qq}")
                        return True
        except Exception as e:
            logger.error(f"POST JSON方法失败: {str(e)}")
        
        # 尝试GET请求带参数
        try:
            full_url = f"{api_base_url}{api_path}"
            logger.info(f"尝试使用GET参数发送消息到 {target_qq}, API地址: {full_url}")
            
            response = requests.get(
                full_url,
                params=params_data,
                timeout=10
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            logger.info(f"API响应内容: {response.text[:200]}...")
            
            # 检查响应
            if response.status_code == 200:
                try:
                    result = response.json()
                    if (result.get("status") == "ok" or 
                        result.get("retcode") == 0 or 
                        result.get("data", {}).get("message_id", None) is not None):
                        logger.info(f"成功发送消息到 {target_qq}")
                        return True
                except:
                    if "success" in response.text.lower():
                        logger.info(f"可能成功发送消息到 {target_qq}")
                        return True
        except Exception as e:
            logger.error(f"GET参数方法失败: {str(e)}")
    
    # 所有API路径和方法都尝试失败
    logger.error(f"所有API路径和方法尝试均失败，无法发送消息到 {target_qq}")
    return False

# 发送邮件通知
def send_email_notification(subject, content):
    # 从环境变量获取邮件配置
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.163.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 25))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    recipient_email = os.environ.get('RECIPIENT_EMAIL', '13708435621@163.com')
    
    if not smtp_user or not smtp_password:
        logger.error("未设置SMTP_USER或SMTP_PASSWORD环境变量，无法发送邮件")
        return False
    
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = smtp_user
        msg['To'] = recipient_email
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [recipient_email], msg.as_string())
        server.quit()
        
        logger.info(f"成功发送邮件通知到 {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"发送邮件失败: {str(e)}")
        return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='发送QQ查寝消息')
    parser.add_argument('--force', action='store_true', help='强制发送消息，忽略时间检查')
    parser.add_argument('--test', action='store_true', help='测试模式，只发送到第一个目标')
    args = parser.parse_args()
    
    # 检查是否强制发送或满足定时条件
    if not args.force and not should_send_now():
        logger.info("当前时间不需要发送查寝消息")
        return
    
    if not QQ_TARGETS:
        logger.error("未设置QQ_TARGETS环境变量")
        return
    
    # 生成三位随机数字
    random_code = f"{random.randint(100, 999)}"
    
    # 查寝消息内容
    message = f"查寝提醒：代码{random_code}，若请假请忽略此条消息，谢谢。"
    
    # 记录成功发送的目标
    success_targets = []
    
    # 获取目标QQ列表
    targets = QQ_TARGETS.split(',')
    
    # 如果是测试模式，只发送给第一个目标
    if args.test and targets:
        logger.info("测试模式：只发送到第一个目标")
        targets = [targets[0]]
    
    # 给每个目标QQ发送消息
    for target in targets:
        target = target.strip()
        if target:
            if send_qq_message(target, message):
                success_targets.append(target)
            # 添加延迟避免频率限制
            time.sleep(1)
    
    # 如果有消息发送成功，发送邮件通知
    if success_targets:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_subject = f"查寝消息发送成功通知 - {now}"
        email_content = f"""
查寝系统消息通知:
发送时间: {now}
验证码: {random_code}
成功发送目标: {', '.join(success_targets)}
        """
        send_email_notification(email_subject, email_content)

if __name__ == "__main__":
    main() 