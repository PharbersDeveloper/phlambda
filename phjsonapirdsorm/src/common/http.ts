import axios from "axios"

export interface IHttp {
    get(url: string): Promise<any>
    post(url: string, parameter: string): Promise<any>
}

export class Http implements IHttp {
    public async get(url: string): Promise<any> {
        return axios({
            auth: {
                username: "demo",
                password: "demo"
            },
            method: "GET",
            url,
            headers: {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json;charset=utf-8"}
        })
    }

    public post(url: string, parameter: any): Promise<any>  {
        return axios({
            auth: {
                username: "demo",
                password: "demo"
            },
            method: "POST",
            url,
            data: JSON.stringify(parameter),
            headers: {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json;charset=utf-8"}
        })
    }
}
