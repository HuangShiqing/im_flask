from wxcloudrun import rest_im

if __name__ == '__main__':
    r = rest_im.account_check("hsqyc")
    print(r)

    rbt = "@RBT#001"
    openid = "oMH9f5RmsMSID5cgw8VAWz1MOUk8"
    r = rest_im.friend_import(openid, rbt)
    print(r)

    r = rest_im.send_txt(rbt, openid, "hi")
    print(r)