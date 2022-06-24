export const awsSdkPromiseResponse = jest.fn().mockReturnValue(Promise.resolve(true));

const putFn = jest.fn().mockImplementation(() => ({ promise: awsSdkPromiseResponse }));
const deleteFn = jest.fn().mockImplementation(() => ({ promise: awsSdkPromiseResponse }));
const getFn = jest.fn().mockImplementation(() => ({ promise: awsSdkPromiseResponse }));
const scanFn = jest.fn().mockImplementation(() => ({ promise: awsSdkPromiseResponse }));

class DocumentClient {
  put = putFn;
  delete = deleteFn;
  get = getFn;
  scan = scanFn;
}

export const DynamoDB = {
  DocumentClient,
};