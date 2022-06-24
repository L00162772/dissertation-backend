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

    let path = event.path
    console.log("path 1:" + path)
    const routeKey = event.httpMethod + ' ' + path
    console.log("routeKey:", routeKey)    
    console.log("path 2:", path)

    let id = path.substring(path.lastIndexOf('/') + 1)
    console.log("id:", id)

    switch (routeKey) { 
      case "GET /health":
        body = "Success";
        break;           
      case "DELETE /users/" + id:
        await dynamo
          .delete({
            TableName: "users",
            Key: {
              id: Number(id)
            }
          })
          .promise();
        body = `Deleted user ${id}`;
        break;
      case "GET /users/" + id:
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
        case "PUT /users/" + id:
          let requestPUTJSON = JSON.parse(event.body);
          await dynamo
            .put({
              TableName: "users",
              Item: {
                id: Number(requestPUTJSON.id),
                firstName: requestPUTJSON.firstName,
                lastName: requestPUTJSON.lastName,
                country: requestPUTJSON.country
              }
            })
            .promise();
          body = `Put user ${requestPUTJSON.id}`;
          break;        
      default:
        throw new Error(`Unsupported route: "${routeKey}"`);
    }
  } catch (err) {
    console.log("err:", err)
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
