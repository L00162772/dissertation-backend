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

    if (event.httpMethod === "OPTIONS") {
      body = "SUCCESS";
      return {
        statusCode,
        body,
        headers
      };
    }

    const routeKey = event.httpMethod + ' ' + event.path
    console.log("routeKey:", routeKey)
    
    switch (routeKey) { 
      case "GET /health":
        body = "Success";
        break;           
      case "DELETE /users/{id}":
        path = event.path
        id = path.substring(path.lastIndexOf('/') + 1)
        await dynamo
          .delete({
            TableName: "users",
            Key: {
              id: id
            }
          })
          .promise();
        body = `Deleted user ${id}`;
        break;
      case "GET /users/{id}":
        path = event.path
        id = path.substring(path.lastIndexOf('/') + 1)
        body = await dynamo
          .get({
            TableName: "users",
            Key: {
              id: id
            }
          })
          .promise();
        break;
      case "GET /users":
        body = await dynamo.scan({ TableName: "users" }).promise();
        break;
      case "POST /users":
        let requestPOSTJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "users",
            Item: {
              id: requestPOSTJSON.id,
              firstName: requestPOSTJSON.firstName,
              lastName: requestPOSTJSON.lastName,
              country: requestPOSTJSON.country
            }
          })
          .promise();
        body = `Post user ${requestPOSTJSON.id}`;
        break;
        case "PUT /users/{id}":
          let requestPUTJSON = JSON.parse(event.body);
          await dynamo
            .put({
              TableName: "users",
              Item: {
                id: requestPOSTJSON.id,
                firstName: requestPUTJSON.firstName,
                lastName: requestPUTJSON.lastName,
                country: requestPUTJSON.country
              }
            })
            .promise();
          body = `Put user ${requestPUTJSON.id}`;
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
