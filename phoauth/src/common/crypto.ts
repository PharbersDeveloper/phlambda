import CryptoJS from "crypto-js"

export default class Crypto {
    hexEncode(value) {
        return value.toString(CryptoJS.enc.Hex)
    }

    hash(value) {
        return CryptoJS.SHA256(value)
    }
}
