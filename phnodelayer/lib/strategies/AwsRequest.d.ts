/// <reference types="node" />
import { IncomingMessage } from 'http';
export default class AWSReq extends IncomingMessage {
    protocol?: string;
    host?: string;
    params?: object;
    query?: object;
    pagination: object;
    body?: object;
    queryStr?: string;
    constructor(event: object, projectName: string);
    private processQueryStringParameters;
}
