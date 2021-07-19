import { GetDatabasesCommand, GlueClient } from "@aws-sdk/client-glue"
export class AWsGlue {
    private client: any = null

    constructor(accessKeyId: string,
                secretAccessKey: string,
                sessionToken: string,
                region: string = "cn-northwest-1") {
       this.client = new GlueClient({
            region,
            credentials: {
                accessKeyId,
                secretAccessKey,
                sessionToken
            }
        })
    }

    public async getDataBases() {
        const command = new GetDatabasesCommand({})
        const result = await this.client.send(command)
        return result.DatabaseList
    }

    public async getTables() {
        return ""
    }

    public async getTable() {
        return ""
    }
}
