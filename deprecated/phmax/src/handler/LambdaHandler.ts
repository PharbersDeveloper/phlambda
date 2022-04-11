import {
    InvokeCommand
} from "@aws-sdk/client-lambda"
import AWSLambda from "../utils/AWSLambda"

export default class LambdaHandler {

    async invokeLambda(functionName: string, args: any) {
        const instance = new AWSLambda()
        const client = instance.getClient()
        const command = new InvokeCommand({
            FunctionName: functionName,
            // InvocationType: "Event",
            Payload: Buffer.from(JSON.stringify(args))
        })
        const aa = await client.send(command)
        console.info(aa)
    }
}
