import { ServerResponse } from "http"
import { AWSRequest } from "phnodelayer"
import GetStepFunctionData from "../common/GetStepFunctionData"
import Register from "../common/Register"
import AWSStepFunction from "../utils/AWSStepFunction"
import AWSSts from "../utils/AWSSts"
import ModelSerialize from "../utils/ModelSerialize"

export default class AppLambdaDelegate {
    async exec(event: any) {
        const projectName = "stepfunction"
        const awsRequest = new AWSRequest(event, projectName)
        const awsResponse = new ServerResponse(awsRequest)
        try {
            const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
            const config = await sts.assumeRole()
            const stepFunctionIns = new AWSStepFunction(config)
            const stepFunctionData = new GetStepFunctionData()
            const register = Register.getInstance
            register.registerEntity(projectName)
            register.registerFunction("functions", stepFunctionData.getStepFunctions)

            if (!event.body) {
                event.body = ""
            }
            const endpoint = event.pathParameters.type
            const queryStringParameters = event.queryStringParameters

            if (endpoint === "functions") {
                const data = await register.getFunc(endpoint)(stepFunctionIns)
                awsResponse["output"] = ["", JSON.stringify(new ModelSerialize().serialize(endpoint, data))]
            }
        } catch (error) {
            awsResponse["output"] = ["", error.message]
            awsResponse["statusCode"] = 500
            const err = new Error()
            err["meta"] = {}
            err["meta"]["response"] = awsResponse
            throw err
        }
        return awsResponse
    }
}
