"use strict"

import S3 from "aws-sdk/clients/s3"
import {AWSError} from "aws-sdk/lib/error"
import phLogger from "../logger/phLogger"

class PhS3Facade {

    private s3 = new S3()

    public listBuckets( bkName: string ) {
        return this.s3.listBuckets().promise()
    }
}

export default new PhS3Facade()
