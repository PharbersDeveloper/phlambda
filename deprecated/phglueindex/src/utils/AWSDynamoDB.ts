
import { DynamoDBClient } from "@aws-sdk/client-dynamodb"

export default class AWSDynamoDB {
    private readonly client: DynamoDBClient = null

    constructor(config: any) {
        this.client = new DynamoDBClient(config)
    }

    getClient() {
        return this.client
    }

    destroy() {
        this.client.destroy()
    }

}
