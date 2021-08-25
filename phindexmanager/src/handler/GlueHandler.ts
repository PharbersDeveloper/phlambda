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
import AWSConfig from "../common/AWSConfig"
import AWSGlue from "../utils/AWSGlue"

export default class GlueHandler {
    private readonly store: IStore
    private config: any = AWSConfig.getInstance.getConf("Pharbers-ETL-Roles")

    constructor(store: IStore) {
        this.store = store
    }

    async exec(event: any) {
        Logger.info("exec")
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
                await this.syncDatabases(dbName)
            }

            for (const table of tableNames) {
                await this.syncTables(table.databaseName, table.tableName)
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

    private async syncDatabases(databaseName: string) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const command = new GetDatabaseCommand({
            Name: databaseName
        })
        const content = await client.send(command)
        instance.destroy()
        const record = {
            name: content.Database.Name,
            provider: content.Database.Parameters?.provider || "pharbers"
        }
        await this.store.create("db", record)
    }

    private async syncTables(databaseName: string, tableName: string) {
        const instance = new AWSGlue(this.config)
        const client = instance.getClient()
        const pageContent = await paginateGetTableVersions({client}, {
            DatabaseName: databaseName,
            TableName: tableName
        })
        const tables = []
        for await (const item of pageContent) {
            const t = item.TableVersions[0]
            tables.push({
                version: t.VersionId,
                provider: t.Table.Parameters?.provider || "pharbers"
            })
        }
        for (const item of tables) {
            const table = await this.store.find("table", null, {match: {database: databaseName, name: tableName}})
            if (table.payload.records.length === 1) {
                const updateRecord = {
                    id: table.payload.records[0].id,
                    replace: {version: item.version}
                }
                await this.store.update("table", updateRecord)
            } else {
                const db = await this.store.find("db", null, {match: {name: databaseName}})
                const record = {
                    name: tableName,
                    version: item.version,
                    database: databaseName,
                    provider: item.provider,
                    db: db.payload.records[0].id
                }
                await this.store.create("table", record)
            }
        }
    }
}