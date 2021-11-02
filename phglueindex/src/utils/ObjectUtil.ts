
export default class ObjectUtil {

    static delObjectKeyIsNull(obj) {
        return Object.keys(obj).map((item) => {
            if (!obj[item]) { delete obj[item] }
            return true
        })
    }

    static generateId() {
        const charset =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
            "abcdefghijklmnopqrstuvwxyz" +
            "0123456789-_"
        const charsetLength = charset.length
        const keyLength = 3 * 5

        // tslint:disable-next-line:one-variable-per-declaration
        let i, array = []

        for (i = 0; i < keyLength; i++) {
            array.push(charset.charAt(Math.floor(Math.random() * charsetLength)))
        }

        return array.join("")

    }

}
