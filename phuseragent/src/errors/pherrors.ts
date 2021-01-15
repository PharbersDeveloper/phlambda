import { ServerResponse } from "http"

interface IPhErrors {
    status: number
    code: number
    headers: any
    message: any
}

export const PhInvalidParameters: IPhErrors = {
    status: 501,
    code: -3,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: JSON.stringify({message: "Invalid Parameters"}),
}

export const PhInvalidClient: IPhErrors = {
    status: 403,
    code: -4,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: JSON.stringify({message: "Invalid Client, Please Contact Pharbers"}),
}

export function errors2response(err: IPhErrors, response: ServerResponse) {
    response.statusCode = err.status
    // @ts-ignore
    response.headers = err.headers
    // @ts-ignore
    response.body = err.message
}