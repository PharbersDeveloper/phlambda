// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

const phlogger = require("./dist_1/logger/phLogger").default
const delegate = require("./dist_1/delegate/appLambdaDelegate").default
// const htmldelegate = require("./dist/delegate/appHtmlDelegate").default

const app = new delegate()
app.prepare()
// const html = new htmldelegate()

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
exports.lambdaHandler = async (event, context) => {
    try {
        phlogger.info(event)
        const result = await app.exec(event)
        // const hdb = await html.queryTemplate("", "")
        const corsHeader =   {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
        response = {
            'statusCode': result.status,
            // 'headers': result.headers,
            'body': result.body
        }
        Object.assign(result.headers, corsHeader)
        response.headers = result.headers
    } catch (err) {
        console.log(err);
        return err;
    }

    return response
};
