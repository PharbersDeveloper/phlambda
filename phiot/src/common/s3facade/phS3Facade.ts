"use strict"

import AWS = require("aws-sdk")
AWS.config.update({
    region: "cn-northwest-1",
    maxRetries: 2,
    httpOptions: {
        timeout: 30000,
        connectTimeout: 5000
    }
})

class PhS3Facade {

    private s3 = new AWS.S3({apiVersion: "2006-03-01"})

    public async listBuckets( bkName: string ) {
        return this.s3.listBuckets().promise()
    }

    public async getObject( bkName: string, key: string) {
        const result = await this.s3.getObject({Bucket: bkName, Key: key }).promise()
        return result.Body
    }

}

export default new PhS3Facade()
