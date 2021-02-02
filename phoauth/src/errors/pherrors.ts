
interface IPhErrors {
    status: number
    code: number
    headers: object
    message: object
}

export const PhNotFoundError: IPhErrors = {
    status: 404,
    code: -1,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Record Not Found" },
}

export const PhInvalidPassword: IPhErrors = {
    status: 403,
    code: -2,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Username or Password is not Valid" },
}

export const PhInvalidParameters: IPhErrors = {
    status: 501,
    code: -3,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Invalid Parameters" },
}

export const PhInvalidAuthGrant: IPhErrors = {
    status: 403,
    code: -4,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Invalid Scope Grant" },
}

export const PhInvalidClient: IPhErrors = {
    status: 403,
    code: -5,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Invalid Client, Please Contact Pharbers" },
}

export const PhInvalidGrantType: IPhErrors = {
    status: 403,
    code: -6,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Invalid Grant Type" },
}

export const PhRecordLoss: IPhErrors = {
    status: 206,
    code: -7,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: { message: "Record Info Loss" },
}

// 在未登录情况下无user_id会重定向到登入页面
export const PhInvalidAuthorizationLogin: IPhErrors = {
    status: 302,
    code: -8,
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "location": ""
    },
    message: { message: "Invalid Authorization Login" },
}

export function errors2response(err: IPhErrors, response: any) {
    response.statusCode = err.status
    // @ts-ignore
    response.headers = err.headers
    // @ts-ignore
    response.body = err.message
}
