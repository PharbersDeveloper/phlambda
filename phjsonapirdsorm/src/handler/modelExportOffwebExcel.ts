import { Logger, SF, Store } from "phnodelayer"

export async function modelExportOffwebExcel(event: Map<string, any>) {
    const postgres = SF.getInstance.get(Store.Postgres)
    await postgres.open()
    const reportsResult = await postgres.find("report")
    Logger.info(reportsResult.payload.records)
    await postgres.close()
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: 200,
        message: {
            message: ""
        }
    }
}
