let response;

const delegate = require("./dist/delegate/appLambdaDelegate").default

const app = new delegate()

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */
exports.lambdaHandler = async function (event, context) {
    try {
        let result

        if (context && context.callbackWaitsForEmptyEventLoop) {
            context.callbackWaitsForEmptyEventLoop = false
        }

        result = await app.exec(event)

        response = {
            'statusCode': result.statusCode,
            'headers': result.output[0],
            'body': String(result.output[1])
        }

        const corsHeader =   {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        }
        let objHeader = {}

        if (typeof result.output[0] === "string") {
            const resultOutput = result.output[0].split("\r\n")
            for (let index = 0; index < resultOutput.length; index++) {
                const element = resultOutput[index].split(":");
                if (element.length === 2) {
                    objHeader[element[0]] = element[1]
                }
            }
        } else {
            objHeader = result.output[0]
        }

        Object.assign(objHeader, corsHeader)
        response.headers = objHeader

    } catch (err) {
        console.error(err);
        return err;
    }

    return response
};
