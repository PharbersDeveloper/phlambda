let response = {}

const corsHeader =   {
  "Access-Control-Allow-Headers" : "Content-Type",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
}
const phLogger = require("phnodelayer").Logger
const delegate = require("./dist/delegate/appLambdaDelegate").default
const accessResponse = require("phauthlayer").Errors2response

const app = new delegate()


const formatResponse = (content) => {
  let objHeader = {}
  let output = null
  const cond = "output" in content || "outputData" in content
  if (cond) {
    output = content.output || content.outputData.map((item) => item.data)
    const resultOutput = output[0].split("\r\n")
    for (let index = 0; index < resultOutput.length; index++) {
      const element = resultOutput[index].split(":");
      if (element.length === 2) {
        objHeader[element[0]] = element[1]
      }
    }
  } else {
    objHeader = content.headers || content.getHeaders()
  }

  Object.assign(objHeader, corsHeader)
  response.statusCode = content.statusCode || content.status
  response.headers = objHeader
  // response.body = "output" in content ? String(content.output[1]) : content.message.message
  if (cond) {
    response.body = String(output[1])
  } else {
    accessResponse(content, response);
    response.body = JSON.stringify(response.body)
  }

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
    if ( !event.queryStringParameters ) {
      event.queryStringParameters = {}
    }
    if ( !event.multiValueQueryStringParameters ) {
      event.multiValueQueryStringParameters = {}
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
