import { Palette } from "../palette";

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

        if (stackSericeLength >= 5) {
            const i = idx % 12
            return this.colorsArr[i]
        } else {
            return this.colorsArr[idx*3+2]
        }

    }

    usedColor(arr, stackSericeLength) {
        const a = this.colorsArr
        if (stackSericeLength >= 5) {
            return a.splice(0,arr.length)
        } else {
            let t = []
            for(let i = 0; i < arr.length; i++) {
                t.push(a[i*3+2])
            }
            return t
        }
    }
}

export default new StackPalette()
