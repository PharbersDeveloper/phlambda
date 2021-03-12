import fortune from "fortune"
import {Http} from "../common/http"

export async function modelExport(event: Map<string, any>) {
    // @ts-ignore
    const versionValue = JSON.parse(event.body).version
    // @ts-ignore
    const idValue = JSON.parse(event.body).owner_id
    const { errors: { BadRequestError } } = fortune
    const airflowRunDagUrl = `http://192.168.112.226:30086/api/v1/dags/dw_export_table/dagRuns`
    const parm = {version: versionValue, owner_id: idValue}
    const res =  await new Http().post(airflowRunDagUrl, {conf: parm})
    if (res.status !== 200) { throw new BadRequestError(res.statusText) }
    return {
        headers: {},
        status: res.status,
        message: {message: "success"}

    }
}
