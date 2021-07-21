import fortune from "fortune"
import {Http} from "../common/http"

export async function entryModelExport(event: Map<string, any>) {
    // @ts-ignore
    const eventBody = JSON.parse(event.body)
    const { errors: { BadRequestError } } = fortune
    const airflowRunDagUrl = `http://192.168.112.226:30086/api/v1/dags/dw_export_table/dagRuns`
    const res =  await new Http().post(airflowRunDagUrl, {conf: eventBody})
    if (res.status !== 200) { throw new BadRequestError(res.statusText) }
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: res.status,
        message: {message: "success"}
    }
}
