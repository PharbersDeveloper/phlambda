let response;

const phLogger = require("phnodelayer").Logger;
const delegate = require("./dist/delegate/appLambdaDelegate").default;

const app = new delegate();

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
      context.callbackWaitsForEmptyEventLoop = false;
    }
    if ( !event.body ) {
      event.body = ""
    }
    const result = await app.exec(event);

    Object.assign(result.headers, {
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
    });
    response = {
      statusCode: result.status || result.statusCode,
      headers: result.headers,
      body: JSON.stringify(result.body),
    };
  } catch (err) {
    phLogger.error(err)
    response = {
      statusCode: err.statusCode,
      headers: {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
      },
      body: JSON.stringify({message: err.message})
    }
  }
  return response;
};
