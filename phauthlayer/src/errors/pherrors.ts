import { ServerResponse } from "http"

interface IPhErrors {
    status: number
    code: number
    headers: object
    message: object
}

export const PhAccessToUnauthorized: IPhErrors = {
    status: 403,
    code: -1,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Access to Unauthorized" },
}

export const PhAccess: IPhErrors = {
    status: 200,
    code: -2,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Access" },
}

export function errors2response(err: IPhErrors, response: ServerResponse) {
    response.statusCode = err.status
    // @ts-ignore
    response.headers = err.headers
    // @ts-ignore
    response.body = err.message
}
