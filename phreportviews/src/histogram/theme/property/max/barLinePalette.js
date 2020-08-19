import { Palette } from "../palette";

export class BarLinePalette extends Palette {
    constructor() {
        super()
        this.colorsArr = [
            "#858D91",
            "#3492E5",
            "#FFCD00",
            "#1C2427"
        ]
    }

    getColors(idx) {
        const arr = this.colorsArr
        return arr[idx]
    }

    usedColor() {
        return this.colorsArr
    }
}

export default new BarLinePalette()
