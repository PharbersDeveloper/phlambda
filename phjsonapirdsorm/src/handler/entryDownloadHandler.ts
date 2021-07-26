import S3 from "aws-sdk/clients/s3"

export async function entryDownloadHandler(event: any) {
    const body = JSON.parse(event.body)
    const bucket = body.bucket || "ph-origin-files"
    const key = body.key
    const s3 = new S3({
        signatureVersion: "v4",
        region: "cn-northwest-1",
        accessKeyId: process.env.AccessKeyId,
        secretAccessKey: process.env.SecretAccessKey
    })
    const params = {Bucket: bucket, Key: key}
    const url = s3.getSignedUrl("getObject", params)
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: 200,
        message: {url}
    }
}

