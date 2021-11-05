from phchangeuserpwd.src.re_password import Re_Passwords


def Run(event, context):
    number = Re_Passwords(event['email'], event['password'], event['new_password']).items()
    for i, j in number:
        if j:
            return i.replace('_', ' ')
    else:
        return '密码更改成功'



