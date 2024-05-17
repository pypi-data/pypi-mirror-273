import websocket
import json
import os
import ssl

ws = None
default_error_tips = "未知错误："
no_login_tips = "用户未登录，无法使用 AI chat 功能，请登录后重试"
error_record = {
    10000000: "操作失败，请稍后重试",
    10000011: "该账户暂未开启 AI chat 体验权限",
    20000001: "失败请重试",
    80000001: "登录态校验失败",
    80000003: "请求参数异常",
    80000004: "AI chat 对话内容涉嫌违规，已结束当前对话，请重新开启对话",
    80000006: "每日使用次数已达上限",
}


def generate_default_error(code: int):
    global default_error_tips, error_record
    return RuntimeError(
        default_error_tips + code
        if code not in error_record.keys()
        else error_record[code]
    )


def parse_message(str: str):
    # print(str)
    if str.startswith("42"):
        data = json.loads(str[2:])
        return {"type": data[0], "payload": data[1]}
    else:
        return {"type": "", "payload": {}}


def stringify_message(type: str, payload: dict):
    return "42" + json.dumps([type, payload])


def join(ws: websocket.WebSocket):
    ws.send(stringify_message("join", {}))
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        if name == "join_ack":
            break


def wait_until_can_join(ws: websocket.WebSocket):
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        payload = data["payload"]
        if name == "server_push_waiting_count":
            print("正在接入AIchat，您前面还有 " + payload["waiting_count"] + " 位用户")
        if name == "server_push_to_join":
            print("您已成功接入AIchat，现在可以开始对话了")
            break


def wait_until_connect(ws: websocket.WebSocket):
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        payload = data["payload"]
        if name != "on_connect_ack":
            continue
        if payload["code"] == 10000012:
            print(
                "正在接入AIchat，您前面还有 "
                + payload["data"]["waiting_count"]
                + " 位用户"
            )
            wait_until_can_join(ws)
        elif payload["code"] != 1:
            ws.close()
            raise generate_default_error(payload["code"])
        join(ws)
        break


def connect():
    global ws
    token = os.environ.get("WOODAI_USER_AUTH")
    env = os.environ.get("WOODAI_RUNTIME_ENV")
    url_prefix = ""
    if env == "dev":
        url_prefix = "dev-"
    elif env == "test":
        url_prefix = "test-"
    elif env == "staging":
        url_prefix = "staging-"
    if token is None:
        raise RuntimeError("用户未登录，无法使用 AI chat 功能，请登录后重试")
    if ws is None or ws.connected is False:
        stag = "3"
        model = "ALIYUN-QWENPTURBO"
        websocket.sock_opt.sslopt = {"cert_reqs": ssl.CERT_NONE}
        ws = websocket.create_connection(
            "ws://"
            + url_prefix
            + "cr-aichat.codemao.cn/aichat/?EIO=3&transport=websocket&stag="
            + stag
            + "&model="
            + model
            + "&token="
            + token
        )
        wait_until_connect(ws)
    return ws


def chat_set(system_role: str = "你是一个友好的AI助手", turn_count: int = 3):
    if len(system_role) > 30:
        raise TypeError("输入过长：请限制在30个字符以内")
    if turn_count > 10 or turn_count < 1:
        raise TypeError("上下文关联数量：仅支持输入1～10个消息数量")
    ws = connect()
    ws.send(
        stringify_message(
            "preset_chat_message",
            {"system_role": system_role, "turn_count": turn_count},
        )
    )
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        if name == "preset_chat_message_ack":
            break


def chat(prompt: str, output=False):
    if len(prompt) > 500:
        raise TypeError("输入过长：请限制在500个字符以内")
    if len(prompt.strip()) == 0:
        raise TypeError("输入不能为空")
    ws = connect()
    ws.send(
        stringify_message("chat", {"messages": [{"role": "user", "content": prompt}]})
    )
    answer = ""
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        payload = data["payload"]
        if name != "chat_ack":
            continue
        if payload["code"] != 1:
            ws.close()
            raise generate_default_error(payload["code"])
        if payload["data"]["content_type"] == "stream_output_begin":
            answer = ""
        if payload["data"]["content_type"] == "stream_output_content":
            answer += payload["data"]["content"]
            if output:
                print(payload["data"]["content"], end="", flush=True)
        if payload["data"]["content_type"] == "stream_output_end":
            if output:
                print("")
            return answer


def chat_clear():
    ws = connect()
    ws.send(stringify_message("clear_chatting_msg", {}))
    while True:
        rec = ws.recv()
        data = parse_message(rec)
        name = data["type"]
        payload = data["payload"]
        if name == "clear_chatting_msg_ack":
            if payload["code"] != 1:
                ws.close()
                raise generate_default_error(payload["code"])
            break
