from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.TLSSigAPIv2 import TLSSigAPIv2
from wxcloudrun.rest_im import account_check, account_import, friend_import, send_txt, api

import json
from flask import Response


@app.route('/', methods=['POST'])
def im_callback():
    """
    :return:
    """
    app.logger.info("get POST request /")
    data = request.get_json()
    rbt = "@RBT#001"
    openid = data["From_Account"]
    CallbackCommand = data["CallbackCommand"]

    if CallbackCommand == "C2C.CallbackAfterSendMsg":
        # 文字, 称呼
        if data["MsgBody"][0]["MsgType"] == "TIMTextElem":
            name = data["MsgBody"][0]["MsgContent"]["Text"]
            r = send_txt(rbt, openid, "收到称呼: {}".format(name))
            # app.logger.info("get name: {}".format(name))
        # 视频, 声音
        elif data["MsgBody"][0]["MsgType"] == "TIMVideoFileElem":
            url = data["MsgBody"][0]["MsgContent"]["VideoUrl"]
            r = send_txt(rbt, openid, "收到视频url: {}".format(url))
            # app.logger.info("get url: {}".format(url))
    return make_succ_response(0)


@app.route('/api/gen_sig')
def gen_sig(methods=['GET']):
    app.logger.info("get request /api/gen_sig")
    rbt = "@RBT#001"
    openid = request.headers["X-Wx-Openid"]

    r = account_check(openid)
    status = r["ResultItem"][0]["AccountStatus"]
    if status != "Imported":
        app.logger.info("openid {} not imported yet".format(openid))
        # 导入用户
        r = account_import(openid)
        if r["ActionStatus"] != "OK":
            pass
        app.logger.info("openid {} imported now".format(openid))

        # 导入好友
        r = friend_import(openid, rbt)
        if r["ResultItem"][0]["ResultCode"] != 0:
            pass
        app.logger.info("{} is {}'s friend now".format(rbt, openid))
    else:
        app.logger.info("openid {} imported".format(openid))

    try_count = 0
    while True:
        r = send_txt(rbt, openid, "你好新朋友, 请分别发送称呼和声音给我")
        if r["ActionStatus"] != "OK":
            app.logger.info("{} send msg to {} not ok".format(rbt, openid))
        else:
            app.logger.info("{} send msg to {} ok".format(rbt, openid))
            break
        try_count += 1
        if try_count >= 5:
            break
    # 在即时通信 IM 控制台-【应用管理】获取 SDKAPPID、SECRETKEY
    # sdkappid = 1600026361
    # secretkey = "5158dd13465291a6db55bbf053803c185a3b805c35b31e2539f3d9a2ff7f98f8"
    # api = TLSSigAPIv2(sdkappid, secretkey)
    sig = api.genUserSig(openid)
    data = json.dumps({"X-Wx-Openid":request.headers["X-Wx-Openid"], "sig":sig})
    return Response(data, mimetype='application/json')


@app.route('/api/return_headers')
def return_headers(methods=['GET']):
    app.logger.info("get request /api/return_headers")
    headers = request.headers
    # print("hsq", headers)
    # app.logger.info('hsq', headers)
    # return make_succ_response(0)
    # data = json.dumps({k:v for k, v in headers.iteritems()})
    data = json.dumps({k:v for k, v in request.headers.items()})
    return Response(data, mimetype='application/json')


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    app.logger.info("get request /")
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    app.logger.info("get POST request /api/count")
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    app.logger.info("get request /api/count")
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
