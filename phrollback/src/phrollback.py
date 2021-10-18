import boto3

def bulid_prefix_of_files(prefix_of_path,provider,version,owner):
    import os
    prefix_of_files = f"provider={provider}/"+f"version={version}/"+f"owner={owner}"
    prefix_of_files = os.path.join(str(prefix_of_path),prefix_of_files)
    return prefix_of_files

def check_file_path(bucket_name,prefix_of_files,provider,version,owner):
    s3 = boto3.resource('s3','cn-northwest-1')
    bucket = s3.Bucket(bucket_name)
    prefix_of_path = bulid_prefix_of_files(prefix_of_files,provider,version,owner)
    process_delete = bucket.objects.filter(Prefix=prefix_of_path)
    #--路径检测
    if len(list(process_delete)) == 0:
        check_response = None
    else:
        check_response = True
    return process_delete,check_response

def rollback(bucket_name,prefix_of_files,provider,version,owner):
    process_delete,check_response = check_file_path(bucket_name,prefix_of_files,provider,version,owner)
    if check_response == True:
        response = process_delete.delete()
    else:
        response = None
    return response

def generate_local_time():
    import time
    current_time = str(time.strftime(r"%Y-%m-%d %H:%M:%S",time.localtime()))
    return current_time

def handle_response(response,bucket_name,prefix_of_files,provider,version,owner):

    current_time = generate_local_time()

    if isinstance(response,list) is True and len(response) == 1:
        item_key = list(response[0].keys())
        if 'Errors' in item_key and len(item_key) == 2 :
            statusCode = 200
            response_info = {'message':list(map(lambda x: x['Message'],response[0]['Errors']))[0],
                             'date':current_time}
        else:
            statusCode = 200
            response_info = { 'message':'success',
                              'date':current_time}
    elif response == None:
        statusCode = 200
        response_info = {'message':"file does not exist,please confirm the file name.",
                         'date': current_time}
    else:
        process_delete,check_response = check_file_path(bucket_name,prefix_of_files,provider,version,owner)
        if check_response == None:
            statusCode = 200
            response_info = {'message':'success',
                             'date':current_time}
        else:
            statusCode = 200
            response_info = {'message':'fail',
                             'data':current_time}
    return statusCode,response_info

def lambda_handler(event,context):
    import json
    event = json.loads(event['body'])
    event = event['parameters']['click_event']
    provider = event["provider_name"]
    version = event["version_name"]
    owner = event["owner_name"]

    bucket_name = "ph-platform"
    prefix_of_files = "2020-11-11/etl/readable_files/clean_source/"
    response = rollback(bucket_name,prefix_of_files,provider,version,owner)
    statusCode,response_info = handle_response(response,bucket_name,prefix_of_files,provider,version,owner)
    return {
        'statusCode': statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        'body': json.dumps({
            'ResponseMetadata': response_info,
        })
    }

