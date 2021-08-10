
import { AssumeRoleCommand, STSClient } from "@aws-sdk/client-sts"

export default class AWSSts {
    private readonly client: STSClient = null
    private readonly region: string = ""

    constructor(accessKeyId: string,
                secretAccessKey: string,
                region: string = "cn-northwest-1",
    ) {
        this.region = region
        this.client = new STSClient({
            region,
            credentials: { accessKeyId, secretAccessKey }
        })
    }

    async assumeRole(name: string = "Pharbers-ETL-Roles",
                     arn: string = "arn:aws-cn:iam::444603803904:role/Pharbers-ETL-Roles") {
        const command = new AssumeRoleCommand({
            RoleArn: arn,
            RoleSessionName: name
        })
        try {
            const result = await this.client.send(command)
            return {
                region: this.region,
                credentials: {
                    accessKeyId: result.Credentials.AccessKeyId,
                    secretAccessKey: result.Credentials.SecretAccessKey,
                    sessionToken: result.Credentials.SessionToken
                }
            }
        } catch (error) {
            throw error
        } finally {
            if (this.client) {this.client.destroy()}
        }
    }
}
