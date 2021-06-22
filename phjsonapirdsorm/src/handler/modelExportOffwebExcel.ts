import { SF, Store } from "phnodelayer"
import * as fs from "fs"
import fortune from "fortune"


export async function modelExportOffwebExcel(event: Map<string, any>) {
    debugger
    console.log("this is export")
    // @ts-ignore
    const postgres = SF.getInstance.get(Store.Postgres)
    await postgres.open()
    const activities = postgres.find('reports', null).then(results => {
        console.log("results", results)
    }).catch(error => {
        console.log("error", error)
    })
    console.log("activities")
    console.log(activities)
    // await postgres.close()
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: 200,
        message: {
            message: ""
        }
    }
}
