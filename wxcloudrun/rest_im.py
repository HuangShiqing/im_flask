import requests, json
from wxcloudrun.TLSSigAPIv2 import TLSSigAPIv2

administrator_userid = "administrator"
sdkappid = 1600026361
secretKey = "5158dd13465291a6db55bbf053803c185a3b805c35b31e2539f3d9a2ff7f98f8"
api = TLSSigAPIv2(sdkappid, secretKey)
administrator_sig = api.genUserSig(administrator_userid)


def account_check(userid):
    cmd = "im_open_login_svc/account_check"
    url = "https://console.tim.qq.com/v4/{}?sdkappid={}&identifier={}&usersig={}&random=99999999&contenttype=json".format(cmd, sdkappid, administrator_userid, administrator_sig)
    data = {
        "CheckItem": [
            {
                "UserID":userid
            }
        ]
    }
    r = requests.post(url, json.dumps(data))
    # print(r.text)
    return r.json()


def account_import(account):
    cmd = "im_open_login_svc/account_import"
    url = "https://console.tim.qq.com/v4/{}?sdkappid={}&identifier={}&usersig={}&random=99999999&contenttype=json".format(cmd, sdkappid, administrator_userid, administrator_sig)
    data = {
        "UserID": account
    }
    r = requests.post(url, json.dumps(data))
    return r.json()


# add to_account as from_account's new friend
def friend_import(from_account, to_account):
    cmd = "sns/friend_import"
    url = "https://console.tim.qq.com/v4/{}?sdkappid={}&identifier={}&usersig={}&random=99999999&contenttype=json".format(cmd, sdkappid, administrator_userid, administrator_sig)
    data = {
        "From_Account": from_account,
        "AddFriendItem": [
            {
                "To_Account": to_account,
                "AddSource": "AddSource_Type_Robot"
            }
        ]
    }
    r = requests.post(url, json.dumps(data))
    return r.json()


def send_txt(send_account, recv_account, text):
    cmd = "openim/sendmsg"
    url = "https://console.tim.qq.com/v4/{}?sdkappid={}&identifier={}&usersig={}&random=99999999&contenttype=json".format(cmd, sdkappid, administrator_userid, administrator_sig)
    data = {
        "SyncOtherMachine": 2,
        "From_Account": send_account,
        "To_Account": recv_account,
        "MsgRandom": 1287657,
        "ForbidCallbackControl":[
            "ForbidBeforeSendMsgCallback",
            "ForbidAfterSendMsgCallback"],
        "MsgBody": [
            {
                "MsgType": "TIMTextElem",
                "MsgContent": {
                    "Text": text
                }
            }
        ],
    }
    r = requests.post(url, json.dumps(data))
    return r.json()

