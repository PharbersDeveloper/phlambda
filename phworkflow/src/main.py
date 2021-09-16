from src.sfn import Sfn

def lambda_handler(event, context):
    # 测试一个codebuild 创建多个lmd
    sfn = Sfn()
    if event['policy'] == 'CreateAndRun':
        create_response = sfn.create_sfn(event)
        machine_arn = create_response.get('stateMachineArn')
        event['machine_arn'] = machine_arn
        sfn.run_sfn(event)
    elif event['policy'] == 'Create':
        sfn.create_sfn(event)
    elif event['policy'] == 'Run':
        sfn.run_sfn(event)