
import GlueCatlogHandler from "./GlueCatlogHandler"

export default class PagePartitionHandler {

    async pageFind(database: string, table: string, nextToken: string, size: number) {
        const gch = new GlueCatlogHandler()
        const partitionContent = await gch.findPartitions(database, table, nextToken, size)
        return {
            data: partitionContent.content.map((item, index) => {
                return {
                    id: index,
                    attributes: {
                        schema: item.schema,
                        attribute: item.attribute
                    },
                    type: "partitions"
                }
            }),
            meta: {
                token: partitionContent.pageToken.slice(0, partitionContent.pageToken.length - 1),
                count: partitionContent.count
            }
        }
    }
}
