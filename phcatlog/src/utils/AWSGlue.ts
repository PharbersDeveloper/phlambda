import {
    GetDatabasesCommand,
    GetPartitionsCommand,
    GetTableCommand,
    GetTablesCommand,
    GlueClient,
    paginateGetDatabases } from "@aws-sdk/client-glue"

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

    public getClient() {
        return this.client
    }
}
