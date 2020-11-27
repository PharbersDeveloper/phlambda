import { Main, logger } from "../index"
import * as fs from "fs"

test(
    "一次错误导致崩溃无法查询数据库",
    async () => {
        const event = JSON.parse(fs.readFileSync("../events/event_common_patch_one.json", "utf8"))

        async function digui() {
            const res = await Main(event)
            logger.info(res)
        }

        try {
            await digui()
        } catch (e) {
            await digui()
        }
    },
    1000 * 60 * 10,
)
