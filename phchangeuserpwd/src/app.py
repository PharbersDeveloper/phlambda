from phchangeuserpwd.src.re_password import Re_Passwords


def Run(event, context):
    print(event)
    number = Re_Passwords(event['id'], event['password'], event['new_password'])
    return number


if __name__ == "__main__":
    import json
    with open("../events/event.json", 'r') as f:
        data = json.load(f)
    data = json.loads(data['body'])
    data['password'] = '1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582'
    print(Run(data, ''))
