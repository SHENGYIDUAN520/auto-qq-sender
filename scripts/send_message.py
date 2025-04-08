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
    # 早上9点整发送查寝消息
    if now.hour == 9 and now.minute == 0:
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
    if not should_send_now():
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
    
    # 给每个目标QQ发送消息
    targets = QQ_TARGETS.split(',')
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