import CryptoJS from "crypto-js"

export default class Crypto {
    public hexEncode(value) {
        return value.toString(CryptoJS.enc.Hex)
    }

    public hash(value) {
        return CryptoJS.SHA256(value)
    }
}
