import fortune from "fortune"
import {Http} from "../common/http"

export async function modelConvert(event: Map<string, any>) {
    // @ts-ignore
    const version = JSON.parse(event.body).version
    const { errors: { BadRequestError } } = fortune
    const airflowRunDagUrl = `http://192.168.112.226:30086/api/v1/dags/dw_dw2db/dagRuns`
    const parm = {version}
    const res =  await new Http().post(airflowRunDagUrl, {conf: parm})
    if (res.status !== 200) { throw new BadRequestError(res.statusText) }
    return {
        headers: {},
        status: res.status,
        message: {message: "success"}

    }
}
