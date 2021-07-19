import fortune from "fortune"
import {Http} from "../common/http"

export async function callRHandler(event: Map<string, any>) {
    const { errors: { BadRequestError } } = fortune
    const airflowRunDagUrl = `http://192.168.112.226:30086/api/v1/dags/ntm/dagRuns`
    // @ts-ignore
    const res =  await new Http().post(airflowRunDagUrl, {conf: JSON.parse(event.body)})
    if (res.status !== 200) { throw new BadRequestError(res.statusText) }
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: res.status,
        message: {
            message: "success",
            status: res.status,
        }
    }
}
