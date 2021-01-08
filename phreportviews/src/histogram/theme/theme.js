
import defaultPalette from "./property/palette"
import defaultPadding from "./property/padding"
import {Position} from "./utils/position"
import {Axis, AxisDirections} from "../axis/axis"
import defaultLabel from "../label/defaultlabel"

export class Theme {
    constructor(
        palette= defaultPalette,
        padding = defaultPadding,
        axis = [
            new Axis(AxisDirections.Left),
            new Axis(AxisDirections.Bottom)
        ],
        label =  defaultLabel) {

        this.palette = palette
        this.padding = padding
        this.axis = axis
        this.label = label
    }

    colors(idx) {
        return this.palette.colors(idx)
    }

    /**
     * define the histogram position with axis
     * @returns {Position}
     */
    histogramRect(pos) {
        const x = pos.x + this.padding.left
        const y = pos.y + this.padding.bottom
        const width = pos.w - this.padding.left - this.padding.right
        const height = pos.h - this.padding.up - this.padding.bottom
        return new Position(x, y, width, height)
    }

    /**
     * define the histogram position without axis
     * @returns {Position}
     */
    histogramInnerRect(pos) {
        const result = new Position(pos.x, pos.y, pos.w, pos.h)
        this.axis.forEach((it) => {
            if (it.isUp()) {
                result.y += it.axisWidth()
            } else if (it.isBottom()) {
                result.h -= it.axisWidth()
            } else if (it.isLeft()) {
                result.x += it.axisWidth()
            } else if (it.isRight()) {
                result.w -= it.axisWidth()
            }
        })
        return result
    }

    queryHorAxis() {
        return this.axis.filter(x => x.isX())
    }

    queryVerAxis() {
        return this.axis.filter(x => x.isY())
    }

    hasLabel() {
        return this.label !== undefined
    }
    queryLabel() {
        return this.label
    }
}

export default new Theme()
