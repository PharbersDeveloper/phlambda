// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

const phlogger = require("./dist/logger/phLogger").default
const delegate = require("./dist/delegate/appLambdaDelegate").default

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

        // Object.assign(result.headers, {
        //     "Access-Control-Allow-Headers" : "Content-Type",
        //     "Access-Control-Allow-Origin": "*",
        //     "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        // })
        response = {
            'statusCode': result.statusCode,
            'headers': result.output[0],
            'body': String(result.output[1])
        }
        // if (response.statusCode === 500 && !app.checkMongoConnection() && tmp === 0) {
        //         phlogger.info("retry connect mongodb for another round.");
        //         tmp = 1
        //         return runLambda(event, context)
        // }
    } catch (err) {
        phlogger.error(err);
        return err;
    }

    return response
};

exports.cleanUp = async () => {
    await app.cleanUp()
};
