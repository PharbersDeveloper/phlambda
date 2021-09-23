import {AssumeRoleCommand, STSClient} from "@aws-sdk/client-sts"
import { AWSRegion } from "../constants/common"

export default class AWSSts {
    private readonly client: STSClient = null

    constructor(accessKeyId: string,
                secretAccessKey: string) {
        this.client = new STSClient({
            region: AWSRegion,
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
                region: AWSRegion,
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
