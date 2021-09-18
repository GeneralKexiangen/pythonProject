
def twilio_send():
    from twilio.rest import Client
    account_sid = 'AC9053e0d5eb1557413f05907e8f202867'
    auth_token = 'b4987948102d4308e89642cf122b99cb'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        #to='+8613487082762',
        to='+8613487082762',
        from_='+18302680260',
        body='Hello, 韩海芳，今天的你最漂亮！小煾煾献上！'
    )
    print(message.body)


def ihuyi_send(text, mobile):
    import http.client as client
    import urllib

    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/notification.php?method=Submit"

    # 查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
    account = "C77914075"
    # 查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
    password = "3af6db87dbf54d4d597a8536cb18d8f4"

    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    print(response_str)
    return response_str


if __name__ == '__main__':
    #twilio_send()
    mobile = "13487082762"
    text = "您的验证码是：121254。请不要把验证码泄露给其他人。"
    ihuyi_send(text, mobile)

