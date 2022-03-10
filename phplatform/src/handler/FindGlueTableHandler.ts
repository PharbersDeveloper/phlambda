import { GetTableCommand } from "@aws-sdk/client-glue"
import AWSGlue from "../utils/AWSGlue"

export default class FindGlueTableHandler {

    async findTable(databaseName: string, name: string) {
        const instance = new AWSGlue()
        const client = await instance.getClient()
        const command = new GetTableCommand({
            DatabaseName: databaseName,
            Name: name
        })
        return await client.send(command)

    }

}
