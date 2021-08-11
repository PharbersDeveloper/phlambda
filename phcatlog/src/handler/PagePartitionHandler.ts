
import GlueCatlogHandler from "./GlueCatlogHandler"

export default class PagePartitionHandler {

    async pageFind(database: string, table: string, nextToken: string) {
        const gch = new GlueCatlogHandler()
        const content = await gch.findPartitions(database, table, nextToken)
        return null
    }
}
