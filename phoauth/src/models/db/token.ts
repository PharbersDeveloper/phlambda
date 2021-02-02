
class Token {
    model: any = {
        authorization: {
            uid: String,
            cid: String,
            code: String,
            redirectUri: String,
            scope: String,
            expired: Date,
        },
        // authorization: {
        //     authorizationCode: String,
        //     expiresAt: Date,
        //     redirectUri: String,
        //     scope: String,
        //     client: Object,
        //     user: Object
        // },
        access: {
            uid: String,
            cid: String,
            token: String,
            refresh: String,
            scope: String,
            expired: Date,
            refreshExpired: Date,
        },
    }
}

export default Token
