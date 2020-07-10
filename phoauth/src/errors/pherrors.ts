import {ServerResponse} from "http"

interface IPhErrors {
    status: number
    code: number
    headers: object,
    message: string
}

export const PhNotFoundError: IPhErrors = {
    status: 404,
    code: -1,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: "Record Not Found"
}

export const PhInvalidPassword: IPhErrors = {
    status: 403,
    code: -2,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: "Username or Password is not Valid"
}

export const PhInvalidParameters: IPhErrors = {
    status: 501,
    code: -3,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: "Invalid Parameters"
}

export const PhInvalidAuthGrant: IPhErrors = {
    status: 403,
    code: -4,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: "Invalid Scope Grant"
}

export const PhInvalidClient: IPhErrors = {
    status: 403,
    code: -4,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: "Invalid Client, Please Contact Pharbers"
}

export function errors2response(err: IPhErrors, response: ServerResponse) {
    response.statusCode = err.status
    // @ts-ignore
    response.headers = err.headers
    // @ts-ignore
    response.body = err.message
}
