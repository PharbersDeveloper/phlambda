import { Palette } from "../palette";

export class MapPalette extends Palette {
    constructor() {
        super()
        this.colorsArr = [
            "#F9D43F",
            "#3492E5",
            "#858D91",
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

export default new MapPalette()
