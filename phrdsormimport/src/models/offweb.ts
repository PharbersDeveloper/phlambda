
const records = {
    activity: {
        title: String,
        subTitle: String,
        startDate: Date,
        endDate: Date,
        location: String,
        city: String,
        activityType: String,
        contentTitle: String,
        contentDesc: String,
        language: Number,
        logo: { link: "image", inverse: "actLogo" },
        logoOnTime: { link: "image", inverse: "actLogoOnTime" },
        gallery: { link: "image", isArray: true, inverse: "actGallery"},
        attachments: { link: "report", isArray: true, inverse: "actAttachments" },
        agendas: { link: "zone", isArray: true, inverse: "actAgendas" },
        partners: { link: "cooperation", isArray: true, inverse: "actPartners" }
    },
    image: {
        path: String,
        tag: String,
        actLogo: { link: "activity", inverse: "logo"},
        actLogoOnTime: { link: "activity", inverse: "logoOnTime"},
        actGallery: { link: "activity", inverse: "gallery"},
        rptCover: { link: "report", inverse: "cover"},
        partAvatar: { link: "participant", isArray: true, inverse: "avatar"},
        coLogo: { link: "cooperation", inverse: "logo"}
    },
    report: {
        title: String,
        subTitle: String,
        description: String,
        cover: { link: "image", inverse: "rptCover"},
        date: Date,
        language: Number,
        writers: { link: "participant", isArray: true, inverse: "writeReports"},
        actAttachments: { link: "activity", isArray: true, inverse: "attachments" }
    },
    participant: {
        name: String,
        title: String,
        occupation: String,
        language: Number,
        writeReports: { link: "report", isArray: true, inverse: "writers"},
        avatar: { link: "image", inverse: "partAvatar"},
        speak: { link: "event", isArray: true, inverse: "speakers"},
        host: { link: "zone", isArray: true, inverse: "hosts" }
    },
    cooperation: {
        name: String,
        companyType: String,
        logo: { link: "image", inverse: "coLogo" },
        language: Number,
        actPartners: { link: "activity", isArray: true, inverse: "partners" }
    },
    event: {
        title: String,
        subTitle: String,
        description: String,
        startDate: Date,
        endDate: Date,
        language: Number,
        speakers: { link: "participant", isArray: true, inverse: "speak" },
        hold: { link: "zone", inverse: "agendas" }
    },
    zone: {
        title: String,
        subTitle: String,
        description: String,
        startDate: Date,
        endDate: Date,
        language: Number,
        hosts: { link: "participant", isArray: true, inverse: "host" },
        agendas: { link: "event", isArray: true, inverse: "hold" },
        actAgendas: { link: "activity", inverse: "agendas" }
    }
}

export default records
