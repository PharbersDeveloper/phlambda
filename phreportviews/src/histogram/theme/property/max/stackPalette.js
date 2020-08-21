import { Palette } from "../palette";
import { color } from "d3";

export class StackPalette extends Palette {
    constructor() {
        super()
        this.colorsArr = [
            "#FFF8AD",
            "#FFF279",
            "#FFEA48",
            "#FFDE17",
            "#FFD219",
            "#FAAF19",
            "#E98A18",
            "#AD6A4F",
            "#8C5B65",
            "#685165",
            "#404864",
            "#454166"
        ]
    }

    getColors(idx, stackSericeLength) {

        if (stackSericeLength <= 5) {
            const colorIndex = 3 + 2 * idx
            return this.colorsArr[colorIndex]
        }

        if (stackSericeLength === 6) {
            const colorIndex = 1 + 2 * idx
            return this.colorsArr[colorIndex]
        }

        if (stackSericeLength <= 8) {
            const subColor = this.colorsArr.slice(3, 3 + stackSericeLength)
            return subColor[idx]
        }

        if(stackSericeLength <= 12) {
            const subColor = this.colorsArr.slice(12 - stackSericeLength)
            return subColor[idx]
        }

    }

    usedColor(arr) {
        const colors = []
        const len = arr.length

        if (len <= 5) {
            for(let i = 0; i < len; i++) {
                colors.push(this.colorsArr[ 3 + 2 * i])
            }
            return colors
        }

        if (len === 6) {
            for(let i = 0; i < len; i++) {
                colors.push(this.colorsArr[ 1 + 2 * i])
            }
            return colors
        }

        if (len <= 8) {
            return this.colorsArr.slice(3, 3 + len)
        }

        if (len <= 12) {
            return this.colorsArr.slice(12 - len)
        }
    }
}

export default new StackPalette()
