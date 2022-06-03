const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  console.log("event:", event)
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*"
  };

  try {
    const routeKey = event.httpMethod + ' ' + event.path
    console.log("routeKey:", routeKey)
    switch (routeKey) { 
      case "GET /health":
        body = "Success";
        break;           
      case "DELETE /users/{id}":
        await dynamo
          .delete({
            TableName: "users",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        body = `Deleted user ${event.pathParameters.id}`;
        break;
      case "GET /users/{id}":
        body = await dynamo
          .get({
            TableName: "users",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        break;
      case "GET /users":
        body = await dynamo.scan({ TableName: "users" }).promise();
        break;
      case "PUT /users":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "users",
            Item: {
              id: requestJSON.id,
              price: requestJSON.price,
              name: requestJSON.name
            }
          })
          .promise();
        body = `Put user ${requestJSON.id}`;
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};
