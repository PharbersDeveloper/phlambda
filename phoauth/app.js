// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

const phlogger = require("./dist/logger/phLogger").default
const delegate = require("./dist/delegate/appLmabdaAuthDelegate").default

const app = new delegate()
app.prepare()

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
        phlogger.info(event)
        // const result = await app.exec(event)
        let result

        if (context && context.callbackWaitsForEmptyEventLoop) {
            context.callbackWaitsForEmptyEventLoop = false
        }

        result = await app.exec(event)
        

        Object.assign(result.headers, {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        })
        response = {
            'statusCode': result.statusCode,
            'headers': result.headers,
        }
        phlogger.info(result)
   
        if (event.pathParameters.edp === "authorization") {
            response["client_id"] = event.queryStringParameters.client_id
        }
    } catch (err) {
        phlogger.error(err);
        return err;
    }
    
    // const clientId = event.queryStringParameters.client_id
    // const responseHeader = response.headers.Location.split("?code=")
    // const responseHeaderRedirectUri = responseHeader[0]
    // const responseHeaderCode = responseHeader[1].split("&state=")[0]
    // const callbackEvent = {
    //     "event": {
    //         "queryStringParameters": {
    //             "redirect_uri": responseHeaderRedirectUri,
    //             "client_id": clientId,
    //             "code": responseHeaderCode,
    //             "grant_type": "authorization_code"
    //         },
    //         "pathParameters": {
    //             "edp": "token"
    //         }
    //     }
    // }
    // const tokenResponse = await app.exec(callbackEvent)
    // return tokenResponse
    return response
    
};

exports.cleanUp = async () => {
    await app.cleanUp()
};
