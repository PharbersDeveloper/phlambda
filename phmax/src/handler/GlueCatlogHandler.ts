import {
    EntityNotFoundException,
    GetTableCommand,
} from "@aws-sdk/client-glue"
import AWsGlue from "../utils/AWSGlue"

export default class GlueCatlogHandler {
    private readonly config: any

    constructor(config: any) {
        this.config = config
    }

    async findTable(name: string, databaseName: string = "phetltemp") {
        try {
            const instance = await new AWsGlue(this.config)
            const client = instance.getClient()
            const command = new GetTableCommand({
                DatabaseName: databaseName,
                Name: name
            })
            const result = await client.send(command)
            return result?.Table?.StorageDescriptor?.Columns || []
        } catch (error) {
            if (error.name === "EntityNotFoundException") {
                return []
            } else {
                throw error
            }
        }
    }
}
