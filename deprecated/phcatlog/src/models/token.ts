class Token {
    model: any = {
        authorization: {
            uid: String,
            cid: String,
            code: String,
            scope: String,
            create: Date,
            expired: Date,
        },
        access: {
            uid: String,
            cid: String,
            token: String,
            refresh: String,
            scope: String,
            create: Date,
            expired: Date,
        },
    }
}

export default Token
