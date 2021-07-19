import {AssumeRoleCommand, STSClient} from "@aws-sdk/client-sts"

export class AWSSts {
    public async assumeRole(accessKeyId: string,
                            secretAccessKey: string,
                            region: string = "cn-northwest-1",
                            roleArn: string = "AKIAWPBDTVEAI6LUCLPX",
                            roleSessionName: string = "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599") {
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
