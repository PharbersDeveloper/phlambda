"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_sts_1 = require("@aws-sdk/client-sts");
class AWSSts {
    constructor(accessKeyId, secretAccessKey, region) {
        this.client = null;
        this.region = "";
        this.region = region;
        this.client = new client_sts_1.STSClient({
            region,
            credentials: { accessKeyId, secretAccessKey }
        });
    }
    async assumeRole(name = "", arn = "") {
        try {
            const result = await this.client.send(new client_sts_1.AssumeRoleCommand({
                RoleArn: arn,
                RoleSessionName: name
            }));
            return {
                region: this.region,
                credentials: {
                    accessKeyId: result.Credentials.AccessKeyId,
                    secretAccessKey: result.Credentials.SecretAccessKey,
                    sessionToken: result.Credentials.SessionToken
                }
            };
        }
        catch (error) {
            throw error;
        }
        finally {
            if (this.client) {
                this.client.destroy();
            }
        }
    }
}
exports.default = AWSSts;
//# sourceMappingURL=AWSSts.js.map