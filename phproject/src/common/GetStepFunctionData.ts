
import {
    ListTagsForResourceCommand,
    paginateListStateMachines} from "@aws-sdk/client-sfn"

export default class GetStepFunctionData {

    async getStepFunctions(clientIns: any,
                           id: string,
                           name: string,
                           provider: string,
                           nextToken: string = "",
                           pageSize: number = 100) {
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
                if (tagsResult.tags.length > 0 && tagsResult.tags.find((tag) => tag.key === "id") !== undefined) {
                    result.push({
                        id: tagsResult.tags.find((tag) => tag.key === "id").value,
                        name: tagsResult.tags.find((tag) => tag.key === "name").value,
                        type: item.type,
                        created: item.creationDate.getTime(),
                        provider: tagsResult.tags.find((tag) => tag.key === "provider").value,
                        tags: tagsResult.tags
                    })
                }
            }
        }
        const filters = {
            id,
            name,
            provider
        }
        for (const item of Object.keys(filters)) {
            if (!filters[item]) {
                delete filters[item]
            }
        }
        const cond = Object.keys(filters).map((key) => {
            return `item["${key}"] === filters["${key}"]`
        }).join(" && ")
        if (cond === "") {
            return result
        }
        // tslint:disable-next-line:no-eval
        return result.filter((item) => eval(cond))
    }
}
