
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
    },
    image: {
        path: String,
        tag: String,
        actLogo: { link: "activity", inverse: "logo"},
        actLogoOnTime: { link: "activity", inverse: "logoOnTime"}
    }
}

export default records
