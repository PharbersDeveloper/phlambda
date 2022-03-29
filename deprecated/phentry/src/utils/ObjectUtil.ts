
export default class ObjectUtil {

    static delObjectKeyIsNull(obj) {
        return Object.keys(obj).map((item) => {
            if (!obj[item]) { delete obj[item] }
            return true
        })
    }

}
