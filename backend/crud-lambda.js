const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  console.log("event:", event)
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json"
  };

  try {
    const routeKey = event.httpMethod + ' ' + event.resource
    console.log("routeKey:", routeKey)
    switch (routeKey) {      
      case "DELETE /users/{id}":
        await dynamo
          .delete({
            TableName: "http-crud-tutorial-users",
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
            TableName: "http-crud-tutorial-users",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        break;
      case "GET /users":
        body = await dynamo.scan({ TableName: "http-crud-tutorial-users" }).promise();
        break;
      case "PUT /users":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "http-crud-tutorial-users",
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
