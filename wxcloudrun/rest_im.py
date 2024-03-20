import requests, json
from wxcloudrun.TLSSigAPIv2 import TLSSigAPIv2

administrator_userid = "administrator"
sdkappid = 1600026361
secretKey = "5158dd13465291a6db55bbf053803c185a3b805c35b31e2539f3d9a2ff7f98f8"
api = TLSSigAPIv2(sdkappid, secretKey)
administrator_sig = api.genUserSig(administrator_userid)


def account_check(userid):
    url = "https://console.tim.qq.com/v4/im_open_login_svc/account_check?sdkappid={}&identifier={}&usersig={}&random=99999999&contenttype=json".format(sdkappid, administrator_userid, administrator_sig)
    data = json.dumps({"CheckItem":[{"UserID":userid}]})
    r = requests.post(url, data)
    # print(r.text)
    return r.json()

if __name__ == '__main__':
    account_check("hsqyc")
