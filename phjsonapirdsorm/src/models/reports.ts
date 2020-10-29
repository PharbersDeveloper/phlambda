// const fields = {
//     year: Number,
//     quarter: Number,
//     month: Number,
//     mkt: String,
//     moleName: String,
//     productName: String,
//     countryName: String,
//     provinceName: String,
//     cityName: String,
//     salesValue: Number,
//     salesQty: Number,
//     prodCurLevel: String,
//     geoCurLevel: String,
//     timeCurLevel: String,
//     prodParpentValue: Number,
//     geoParpentValue: Number,
//     timeParpentValue: Number,
//     prodPpValue: Number,
//     lattles: String,
//     marketShare: Number,
//     moleShare: Number,
//     prodMoleShare: Number,
//     timeProviousValue: Number,
//     timeProviousShareValue: Number,
//     marketSalesGrowth: Number,
//     salesGrowth: Number,
//     ei: Number,
// }
// class Reports {
//     public model: any = {
//         aohong: fields,
//         astellas: fields,
//         az: fields,
//         beite: fields,
//         gilead: fields,
//         haikun: fields,
//         huiyu: fields,
//         jingxin: fields,
//         kangzhe: fields,
//         mylan: fields,
//         nhwa: fields,
//         pfizer: fields,
//         qilu: fields,
//         sankyo: fields,
//         sanofi: fields,
//         servier: fields,
//         tide: fields,
//         xlt: fields
//     }
// }
//
// export default Reports

class Reports {
    public model: any = {
        template: {
            parent: { link: "template", isArray: true, inverse: "child" },
            child: { link: "template", isArray: true, inverse: "parent" },
            partnerTemplate: {link: "partner", inverse: "templates"},
            name: String,
            source: String,
            rid: String,
            gid: String,
            tag: String,
            version: String,
            description: String,
            created: Date,
            modified: Date
        },
        partner: {
            pid: String,
            templates: { link: "template", isArray: true, inverse: "partnerTemplate" },
            created: Date,
            modified: Date
        }
    }

    public operations = {
        hooks: {
            template: [ this.hooksDate ],
            partner: [ this.hooksDate ]
        }
    }

    protected hooksDate(context, record, update) {
        const { request: { method, meta: { language } } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                return record
            case "update":
                update.replace.modified = new Date()
                return update
        }
    }
}

export default Reports
