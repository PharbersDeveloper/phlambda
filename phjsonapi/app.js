// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

const phlogger = require("./dist/logger/phLogger").default
const delegate = require("./dist/delegate/appLambdaDelegate").default

const app = new delegate()
app.prepare()

let tmp = 0

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
        // const result = await app.exec(event)
        let result

        if (event.importDataFromExcel) {
            result = await app.excelImportData(event)
        } else {
            result = await app.exec(event)
            tmp = 0
        }

        response = {
            'statusCode': result.status,
            'headers': result.headers,
            'body': result.body
        }
    } catch (err) {
        phlogger.error(err);
        if (!app.checkMongoConnection() && tmp === 0) {
            phlogger.info("retry connect mongodb for another round.");
            tmp = 1
            return lambdaHandler(event, context)
        }
        return err;
    }

    return response
};
