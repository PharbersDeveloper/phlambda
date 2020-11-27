
let response = {}

const corsHeader =   {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
}
const phLogger = require("phnodelayer").logger
const delegate = require("./dist/delegate/appLambdaDelegate").default

const app = new delegate()


const formatResponse = (content) => {
    let objHeader = {}
    response.statusCode = content.statusCode
    response.headers = content.output[0]
    response.body = String(content.output[1])

    const resultOutput = content.output[0].split("\r\n")
    for (let index = 0; index < resultOutput.length; index++) {
        const element = resultOutput[index].split(":");
        if (element.length === 2) {
            objHeader[element[0]] = element[1]
        }
    }

    Object.assign(objHeader, corsHeader)
    response.headers = objHeader
}
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
        if (context && context.callbackWaitsForEmptyEventLoop) {
            context.callbackWaitsForEmptyEventLoop = false
        }
        if ( !event.body ) {
            event.body = ""
        }
        const result = await app.exec(event)
        if (result) {
            formatResponse(result)
        }

    } catch (err) {
        if ("meta" in err) {
            formatResponse(err.meta.response)
        } else {
            phLogger.error(err);
            return err;
        }
    }

    return response
};
