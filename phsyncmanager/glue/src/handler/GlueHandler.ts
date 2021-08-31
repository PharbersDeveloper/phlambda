import {
    GetDatabaseCommand,
    GetTableCommand,
    paginateGetDatabases,
    paginateGetPartitions,
    paginateGetTables,
    paginateGetTableVersions,
    UpdateTableCommand
} from "@aws-sdk/client-glue"
import {IStore, Logger} from "phnodelayer"
import AWSGlue from "../utils/AWSGlue"

export default class GlueHandler {
    private readonly store: IStore
    private readonly config: any

    constructor(store: IStore, config: any) {
        this.store = store
        this.config = config
    }

    async exec(event: any) {
        for ( const item of event.Records ) {
            const subject = item?.Sns?.Subject || undefined
            const message = item?.Sns?.Message || undefined
            const attributes = item?.Sns?.MessageAttributes || undefined
            if (message && attributes && subject === "glueindex") {
                switch (attributes.type.Value) {
                    case "database":
                        await this.syncDatabases(JSON.parse(message).name, attributes.action.Value)
                        break
                    case "table":
                        const { name, database } = JSON.parse(message)
                        await this.syncTables(database, name, attributes.action.Value)
                        break
                }
            }
        }
    }

    async syncAll(updatePartitionCount: boolean = false) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const pageDataBaseContent = await paginateGetDatabases({client}, {})
        const databaseNames = []
        const tableNames = []
        for await (const item of pageDataBaseContent) {
            item.DatabaseList.forEach((database) => {
                databaseNames.push(database.Name)
            })
        }

        for (const dbName of databaseNames) {
            const pageTableContent = await paginateGetTables({client}, { DatabaseName: dbName })
            for await (const item of pageTableContent) {
                item.TableList.forEach((table) => {
                    tableNames.push({
                        databaseName: table.DatabaseName,
                        tableName: table.Name
                    })
                })
            }
        }

        if (updatePartitionCount) {
            for (const table of tableNames) {
                await this.addPartitionCountToTableAttr(table.databaseName, table.tableName)
            }
        } else {
            for (const dbName of databaseNames) {
                await this.syncDatabases(dbName, "create")
            }

            for (const table of tableNames) {
                await this.syncTables(table.databaseName, table.tableName, "create")
            }
        }
    }

    private async addPartitionCountToTableAttr(databaseName: string, tableName: string) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const partitions = await paginateGetPartitions({client}, {
            DatabaseName: databaseName,
            TableName: tableName
        })
        const partitionCountArr = []
        for await (const item of partitions) {
            partitionCountArr.push(item.Partitions.length)
        }
        const partitionCount = partitionCountArr.reduce((sum, current) => sum + current).toString() || "0"
        const getTableCommand = new GetTableCommand({
            DatabaseName: databaseName,
            Name: tableName
        })
        console.info(`database => ${databaseName}  table => ${tableName}   partitionCount => ${partitionCount}`)
        const getTable = await client.send(getTableCommand)
        const tableInput = getTable.Table
        if (tableInput.Parameters === undefined) {
            tableInput.Parameters = {}
        }
        tableInput.Parameters.partitionCount = partitionCount

        const updateCommand = new UpdateTableCommand({
            DatabaseName: databaseName,
            TableInput: tableInput
        })
        await client.send(updateCommand)
    }

    private async syncDatabases(databaseName: string, action: string) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const command = new GetDatabaseCommand({
            Name: databaseName
        })
        const content = await client.send(command)
        switch (action) {
            case "create":
                const record = {
                    name: content.Database.Name,
                    provider: content.Database.Parameters?.provider || "pharbers"
                }
                await this.store.create("db", record)
                break
            case "delete":
                const dt = await this.store.find("db", null, {match: {name: databaseName}})
                await this.store.delete("db", dt.payload.records[0].id)
                await this.store.delete("table", dt.payload.records[0].tables)
                break
        }
    }

    private async syncTables(databaseName: string, tableName: string, action: string) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const pageContent = await paginateGetTableVersions({client}, {
            DatabaseName: databaseName,
            TableName: tableName
        })
        const lastTable = (await pageContent.next()).value.TableVersions[0]
        switch (action) {
            case "create":
                await this.addPartitionCountToTableAttr(databaseName, tableName)
                const db = await this.store.find("db", null, {match: {name: databaseName}})
                const record = {
                    name: tableName,
                    version: lastTable.VersionId,
                    database: databaseName,
                    provider: lastTable.Table.Parameters?.provider || "pharbers",
                    db: db.payload.records[0].id
                }
                await this.store.create("table", record)
                break
            case "update":
                await this.addPartitionCountToTableAttr(databaseName, tableName)
                const table = await this.store.find("table", null, {match: {database: databaseName, name: tableName}})
                const updateRecord = {
                    id: table.payload.records[0].id,
                    replace: {version: lastTable.VersionId}
                }
                await this.store.update("table", updateRecord)
                break
            case "delete":
                const dt = await this.store.find("table", null, {match: {database: databaseName, name: tableName}})
                await this.store.delete("table", dt.payload.records[0].id)
                break
        }
    }
}
