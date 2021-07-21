import {AssumeRoleCommand, STSClient} from "@aws-sdk/client-sts"

export class AWSSts {
    async assumeRole(accessKeyId: string,
                            secretAccessKey: string,
                            region: string = "cn-northwest-1",
                            roleArn: string = "arn:aws-cn:iam::444603803904:role/Pharbers-ETL-Roles",
                            roleSessionName: string = "Pharbers-ETL-Roles") {
        const client = new STSClient({
            region,
            credentials: { accessKeyId, secretAccessKey }
        })

        const command = new AssumeRoleCommand({
            RoleArn: roleArn,
            RoleSessionName: roleSessionName
        })
        try {
            const result = await client.send(command)
            return result.Credentials
        } catch (error) {
            throw error
        } finally {
            client.destroy()
        }
    }
}
