import {AssumeRoleCommand, STSClient} from "@aws-sdk/client-sts"

export default class AWSSts {
    private readonly client: STSClient = null
    private readonly region: string = ""

    constructor(accessKeyId: string,
                secretAccessKey: string,
                region: string,
    ) {
        this.region = region
        this.client = new STSClient({
            region,
            credentials: { accessKeyId, secretAccessKey }
        })
    }

    async assumeRole(name: string = "", arn: string = "") {
        try {
            const result = await this.client.send(new AssumeRoleCommand({
                RoleArn: arn,
                RoleSessionName: name
            }))
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
