import { APIGatewayProxyEvent } from "aws-lambda";
import { DynamoDB } from './__mocks__/aws-sdk';
const db = new DynamoDB.DocumentClient();

const app = require('../crud-lambda.js');

describe('Unit test for app handler', function () {
    it('verifies unknown route', async () => {
        const event: APIGatewayProxyEvent = {
            httpMethod: "GET",
            path: "/unknown"
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(400);
    });

    it('verifies OPTIONS successful response', async () => {
        const event: APIGatewayProxyEvent = {
            httpMethod: "OPTIONS"
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
    });

    it('verifies GET Health successful response', async () => {
        const event: APIGatewayProxyEvent = {
            httpMethod: "GET",
            path: "/health"
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
    });  
    

    it('verifies DELETE User successful response', async () => {
        const id = 1
        const event: APIGatewayProxyEvent = {
            httpMethod: "DELETE",
            path: "/users/" + id
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
        expect(db.delete).toHaveBeenCalledWith({ TableName: 'users', Key: {id: id} });
    });     

    it('verifies GET Users successful response', async () => {
        const id = 1
        const event: APIGatewayProxyEvent = {
            httpMethod: "GET",
            path: "/users/" + id
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
        const idStr = "" + id
        expect(db.get).toHaveBeenCalledWith({ TableName: 'users', Key: {id: idStr} });
    }); 

    it('verifies GET All Users successful response', async () => {
        const event: APIGatewayProxyEvent = {
            httpMethod: "GET",
            path: "/users"
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
        expect(db.scan).toHaveBeenCalledWith({ TableName: 'users'});
    });   
    

    it('verifies POST Create User successful response', async () => {
        const body = {
            id: 1,
            firstName: "Joe",
            lastName: "Bloggs",
            country: "Ireland"
        }
        const event: APIGatewayProxyEvent = {
            httpMethod: "POST",
            path: "/users",
            body: JSON.stringify(body)
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
        expect(db.put).toHaveBeenCalledWith({ TableName: 'users', Item: {
            id: body.id,
            firstName: body.firstName,
            lastName: body.lastName,
            country: body.country
          }});
    });   
    
    it('verifies PUT Update User successful response', async () => {
        const id = 1
        const body = {
            id: id,
            firstName: "Joe",
            lastName: "Bloggs",
            country: "Ireland"
        }
        const event: APIGatewayProxyEvent = {
            httpMethod: "PUT",
            path: "/users/" + id,
            body: JSON.stringify(body)
        } as any
        const result = await app.handler(event)

        expect(result.statusCode).toEqual(200);
        expect(db.put).toHaveBeenCalledWith({ TableName: 'users', Item: {
            id: body.id,
            firstName: body.firstName,
            lastName: body.lastName,
            country: body.country
          }});
    });    
    
});