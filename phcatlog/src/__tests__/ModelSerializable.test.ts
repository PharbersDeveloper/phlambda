import {Serializer} from "jsonapi-serializer"
import GetGlueData from "../common/getGlueData"
import ModelSerialize from "../common/modelSerialize"
import Register from "../common/register"
import Catlog from "../models/catlog"
import {AWsGlue} from "../utils/AWSGlue"
import {AWSSts} from "../utils/AWSSts"

test("Test jsonapi-serializer Library", async () => {
    const sts = new AWSSts()
    const result = await sts.assumeRole("AKIAWPBDTVEAI6LUCLPX",
        "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599")
    const glueIns = new AWsGlue(result.AccessKeyId, result.SecretAccessKey, result.SessionToken)
    const getGlueData = new GetGlueData()

    const register = Register.getInstance
    register.registerEntity("catlog")
    register.registerFunction("database", getGlueData.getDataBases)
    register.registerFunction("tables", getGlueData.getTables)
    register.registerFunction("partitions", getGlueData.getPartitions)

    const data = await register.getFunc("tables")(glueIns, "phdatacat")
    const serialize = new ModelSerialize()
    const res = serialize.serialize("tables", data)
    console.info(JSON.stringify(res, null, "\t"))


    // const listDataBase = await glue.getDataBases()
    // const catlog = new Catlog()
    // const model = listDataBase.map((item) => {
    //     catlog.model[modelName] = item
    //     return catlog.model
    // })
    // console.info(model[0][modelName])

    // const DataBaseSerializer = new Serializer("database", {
    //     attributes: Object.keys(listDataBase[0])
    // })
    // const database = DataBaseSerializer.serialize(listDataBase)
    // console.info(JSON.stringify(database, null, "\t"))
    //
    // const listTable = await glue.getTables("phdatacat")
    // const TableSerializer = new Serializer("table", {
    //     attributes: Object.keys(listTable[0])
    // })
    // const table = TableSerializer.serialize(listTable)
    // console.info(JSON.stringify(table, null, "\t"))
    //
    // const listPartition = await glue.getPartition("phdatacat", "chemdata")
    // const PartitionSerializer = new Serializer("partition", {
    //     attributes: Object.keys(listPartition[0])
    // })
    // const partition = PartitionSerializer.serialize(listPartition)
    // console.info(JSON.stringify(partition, null, "\t"))

    // const data = [
    //     {
    //         id: "1",
    //         name: "Alex",
    //         address: [
    //             {
    //                 id: "1",
    //                 name: "Fuck"
    //             }
    //         ]
    //     }
    // ]
    //
    // const UserSerializer = new Serializer("user", {
    //     attributes: ["name", "address"],
    //     address: {
    //         ref: "id",
    //         included: true,
    //         attributes: ["name"]
    //     }
    // })
    //
    // console.info(JSON.stringify(UserSerializer.serialize(data), null, "\t"))

}, 1000 * 60 * 10)
