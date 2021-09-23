import {
    GetObjectTaggingCommand,
    PutObjectCommand,
    PutObjectTaggingCommand,
    PutObjectTaggingCommandInput } from "@aws-sdk/client-s3"
import * as fs from "fs"
import { Logger } from "phnodelayer"
import AWsS3 from "../utils/AWSS3"

export default class S3Handler {

    async putFile(bucket: string, key: string, path: string, tags: string) {
        const instance = await new AWsS3()
        const client = instance.getClient()
        const buffer = fs.readFileSync(path)
        const command = new PutObjectCommand({
            Bucket: bucket,
            Key: key,
            Body: buffer,
            Tagging: tags
        })
        await client.send(command)

    }

    async putTags(bucket: string, key: string, tags: any) {
        const instance = await new AWsS3()
        const client = instance.getClient()
        const findTags = await this.findTags(bucket, key)

        const finalTags = findTags.concat(tags).reduce((prev, current, index, array) => {
            if (!(current.Key in prev.keys)) {
                prev.keys[current.Key] = index
                prev.result.push(current)
            } else {
                prev.result[prev.keys[current.Key]] = current
            }
            return prev
        }, {result: [], keys: {}})

        const command = new PutObjectTaggingCommand({
            Bucket: bucket,
            Key: key,
            Tagging: {
                TagSet: finalTags.result
            }
        })
        await client.send(command)
    }

    private async findTags(bucket: string, key: string) {
        try {
            const instance = await new AWsS3()
            const client = instance.getClient()
            const command = new GetObjectTaggingCommand({
                Bucket: bucket,
                Key: key
            })
            const result = await client.send(command)
            return result?.TagSet || []
        } catch (error) {
            Logger.error(error)
            return []
        }
    }
}
