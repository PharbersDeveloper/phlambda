"use strict"
import * as R from "ramda"
import phLogger from "../logger/phLogger"
import Asset from "../models/entry/Asset"
import DataSet from "../models/entry/DataSet"
import DbSource from "../models/entry/DbSource"
import File from "../models/entry/File"
import Job from "../models/entry/Job"
import Mart from "../models/entry/Mart"

export default async function mongo2postgres(mongo, store) {
    const fm = new File().getModel()
    const fmr = await fm.find()
    const files = await Promise.all(fmr.map (async (doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        // record.id = tmp
        const isr = await store.create("file", record)
        return {
            id: tmp,
            dbid: isr.payload.records[0].id,
            extension: isr.payload.records[0].extension,
            size: isr.payload.records[0].size,
            url: isr.payload.records[0].url,
            createdTime: new Date()
        }
    }))
    phLogger.info(files)

    const jm = new Job().getModel()
    const jmr = await jm.find()
    const jobs = await Promise.all(jmr.map (async (doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        // record.id = tmp
        if (record.create) {
            record.create = new Date(record.create)
        } else {
            record.create = new Date()
        }
        const isr = await store.create("job", record)
        return { id: tmp, dbid: isr.payload.records[0].id }
    }))
    phLogger.info(jobs)

    const dm = new DbSource().getModel()
    const dmr = await dm.find()
    const dbs = await Promise.all(dmr.map (async (doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        // record.id = tmp
        if (record.create) {
            record.create = new Date(record.create)
        } else {
            record.create = new Date()
        }
        const isr = await store.create("dbSource", record)
        return { id: tmp, dbid: isr.payload.records[0].id }
    }))
    phLogger.info(dbs)

    const dfm = new DataSet().getModel()
    const dfr = await dfm.find()
    const records = dfr.map ((doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        record.id = tmp

        // @ts-ignore
        const j = jobs.find((x) => x.id === record.job)
        if (j) {
            // @ts-ignore
            record.job = j.dbid
        } else {
            delete record.job
        }
        record.parent = record.parent.map((p) => p.toString())
        return record
    })
    const dfs = []
    const inserted = []
    while (inserted.length !== records.length) {
        await Promise.all(records.map (async (record) => {
            // if (record._id === undefined) {
            //     return
            // }
            // const tmp = record._id.toString()
            // delete record._id
            // delete record.__v
            // record.id = tmp

            if (inserted.indexOf(record.id) === -1) {
                if (record.parent.length === 0) {
                    const isr = await store.create("dataSet", record)
                    dfs.push({ id: record.id, dbid: isr.payload.records[0].id })
                    inserted.push(isr.payload.records[0].id)
                } else if (record.parent.map((p) => inserted.indexOf(p) !== -1)
                    .reduce((prev, curr, idx, arr) => prev + curr) === record.parent.length) {
                    const isr = await store.create("dataSet", record)
                    dfs.push({ id: record.id, dbid: isr.payload.records[0].id })
                    inserted.push(isr.payload.records[0].id)
                } else {
                    record.parent = []
                }
            }
        }))
    }
    phLogger.info(dfs)

    const mm = new Mart().getModel()
    const mmr = await mm.find()
    const mms = await Promise.all(mmr.map (async (doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        // record.id = tmp

        record.dfs = record.dfs.map((x) => x.toString())
        record.dfs.map((r) => {
            const t = dfs.find((x) => x.id === r.id)
            if (t) { return t }
            return undefined
        }).filter((x) => x !== undefined)

        const isr = await store.create("mart", record)
        return { id: tmp, dbid: isr.payload.records[0].id }
    }))
    phLogger.info(mms)

    const am = new Asset().getModel()
    const amr = await am.find()
    const ams = await Promise.all(amr.map (async (doc) => {
        const record = doc._doc
        const tmp = record._id.toString()
        delete record._id
        delete record.__v
        // record.id = tmp

        if (record.createTime) {
            record.createTime = new Date(record.createTime)
        } else {
            record.createTime = new Date()
        }

        record.dfs = record.dfs.map((x) => x.toString())
        record.dfs.map((r) => {
            const t = dfs.find((x) => x.id === r.id)
            if (t) { return t }
            return undefined
        }).filter((x) => x !== undefined)

        let url: string
        let extension: string
        let createdTime: Date
        let size: number
        if (record.file) {
            const fn = record.file.toString()
            // @ts-ignore
            const f = files.find((x) => x.id === fn)
            if (f) {
                // @ts-ignore
                record.file = f.dbid
                // @ts-ignore
                url = f.url
                // @ts-ignore
                createdTime = f.createdTime
                // @ts-ignore
                size = f.size
                // @ts-ignore
                extension = f.extension
            } else { delete record.file }
        }

        if (record.dbs) {
            const dbn = record.dbs.toString()
            // @ts-ignore
            const db = dbs.find((x) => x.id === dbn)
            // @ts-ignore
            if (db) { record.dbs = db.dbid } else { delete record.dbs }
        }

        if (record.mart) {
            const mn = record.mart.toString()
            // @ts-ignore
            const m = mms.find((x) => x.id === mn)
            // @ts-ignore
            if (m) { record.mart = m.dbid } else { delete record.mart }
        }

        const isr = await store.create("asset", record)
        return {
            id: tmp,
            dbid: isr.payload.records[0].id,
            owner: isr.payload.records[0].owner,
            fileName: isr.payload.records[0].name,
            martTags: isr.payload.records[0].martTags,
            providers: isr.payload.records[0].providers,
            markets: isr.payload.records[0].markets,
            molecules: isr.payload.records[0].molecules,
            dataCover: isr.payload.records[0].dataCover,
            geoCover: isr.payload.records[0].geoCover,
            labels: isr.payload.records[0].labels,
            url,
            createdTime,
            size,
            extension
        }
    }))
    phLogger.info(ams)

    /**
     * 0. fileIndex for web page
     */
    // @ts-ignore
    const byFileName = R.groupBy((at: object) => at.fileName)
    // @ts-ignore
    const fileIndex = byFileName(ams)
    // @ts-ignore
    const fir = await Promise.all(R.keys(fileIndex).map (async (fn: string) => {
        const farray = fileIndex[fn]
        const record = {
            fileName: fn,
            // @ts-ignore
            owner: R.head(farray.map((x) => x.owner)),
            // @ts-ignore
            martTags: R.uniq(R.flatten(farray.map((x) => x.martTags))),
            // @ts-ignore
            providers: R.uniq(R.flatten(farray.map((x) => x.providers))),
            // @ts-ignore
            markets: R.uniq(R.flatten(farray.map((x) => x.markets))),
            // @ts-ignore
            molecules: R.uniq(R.flatten(farray.map((x) => x.molecules))),
            // @ts-ignore
            dataCover: R.uniq(R.flatten(farray.map((x) => x.dataCover))),
            // @ts-ignore
            geoCover: R.uniq(R.flatten(farray.map((x) => x.geoCover))),
            // @ts-ignore
            labels: R.uniq(R.flatten(farray.map((x) => x.labels))),
            // @ts-ignore
            assets: R.uniq(farray.map((x) => x.dbid)),
            // @ts-ignore
            url: R.head(farray.map((x) => x.url)),
            // @ts-ignore
            extension: R.head(farray.map((x) => x.extension)),
            // @ts-ignore
            createdTime: R.head(farray.map((x) => x.createdTime)),
            // @ts-ignore
            size: R.head(farray.map((x) => x.size)),
        }
        // phLogger.info(doc.fileName)
        if (record.url === undefined) {
            record.url = null
        }

        if (record.createdTime === undefined) {
            record.createdTime = new Date()
        }

        if (record.size === undefined) {
            record.size = -1
        }

        if (record.extension === undefined) {
            record.extension = null
        }

        const isr = await store.create("fileIndex", record)
        return { id: isr.payload.records[0].id, dbid: isr.payload.records[0].id }
    }))
    phLogger.info(fir)
}
