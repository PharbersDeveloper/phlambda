
import {
    ListTagsForResourceCommand,
    paginateListStateMachines} from "@aws-sdk/client-sfn"

export default class GetStepFunctionData {

    async getStepFunctions(clientIns: any,
                           nextToken: string,
                           pageSize: number = 10) {
        const client = clientIns.getClient()
        const paginator = paginateListStateMachines({
                        client,
                        pageSize,
                        startingToken: nextToken
                    }, {})

        const result = []
        const pageData = await paginator.next()
        if (pageData.value) {
            for (const item of pageData.value.stateMachines) {
                const command = new ListTagsForResourceCommand({ resourceArn: item.stateMachineArn })
                const tagsResult = await client.send(command)
                result.push({
                    name: item.name,
                    type: item.type,
                    created: item.creationDate.getTime(),
                    tags: tagsResult.tags
                })
            }
        }
        return result
    }
}
