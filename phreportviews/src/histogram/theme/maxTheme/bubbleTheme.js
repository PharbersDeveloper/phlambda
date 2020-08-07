
import BubblePalette from "../property/max/bubblePalette"
import defaultPadding from "../property/padding"
import {Position} from "../utils/position"
// import {Axis, AxisDirections} from "../../axis/axis"
import {MaxAxis, AxisDirections} from "../../axis/maxAxis/maxAxis"
import defaultLabel from "../../label/defaultlabel"
import BubbleLabel from "../../label/maxLabel/bubbleLabel"

export class BubbleTheme {
    constructor(
        palette= BubblePalette,
        padding = defaultPadding,
        axis = [
            new MaxAxis(AxisDirections.Left),
            new MaxAxis(AxisDirections.Bottom)
        ],
        label =  BubbleLabel) {

        this.palette = palette
        this.padding = padding
        this.axis = axis
        this.label = label
    }

    createColors(svg) {
        this.palette.renderRadia(svg)
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
                result.h -= it.axisWidth() + 40
            } else if (it.isLeft()) {
                result.x += it.axisWidth() + 40
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

    xTitlePosition() {

    }

    axisAssist(svg, ivp) {
        this.axis[0].renderBackgroundLine(svg, ivp)
    }

    showLabel(svg, ivp) {
        this.label.render(svg, ivp)
    }

    setXAxisTicks(min, max, n) {
        this.queryHorAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    setYAxisTicks(min, max, n) {
        this.queryVerAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    clipBubbleChart(svg, ivp) {
        this.axis[0].clipChart(svg, ivp)
    }
}

export default new BubbleTheme()
