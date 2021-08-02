
import { ListStateMachinesCommand,
    ListTagsForResourceCommand,
    paginateListStateMachines,
    SFNPaginationConfiguration } from "@aws-sdk/client-sfn"

import AWSStepFunction from "../utils/AWSStepFunction"
import AWSSts from "../utils/AWSSts"

test("Get Step Functions", async () => {
    const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
    const config = await sts.assumeRole()
    const stepFunctionIns = new AWSStepFunction(config)
    const client = stepFunctionIns.getClient()
    let nextToken = ""
    const paginator = paginateListStateMachines({
        client,
        pageSize: 10,
        startingToken: nextToken
    }, {})

    const pageData = await paginator.next()
    for (const item of pageData.value.stateMachines) {
        const command = new ListTagsForResourceCommand({
            resourceArn: item.stateMachineArn
        })
        const result = await client.send(command)
        console.info(JSON.stringify(result.tags))
    }

    // console.info(pageData)

    // const command = new ListTagsForResourceCommand({
    //     resourceArn: "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:ETL_Iterator"
    // })
    // const result = await client.send(command)
    // console.info(result)
})
