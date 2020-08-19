
import StackPalette from "../property/max/StackPalette"
import Theme from "../theme"
import defaultPadding from "../property/padding"
import StackPadding from "../property/max/stackPadding"
import {Position} from "../utils/position"
import {MaxStackAxis, AxisDirections} from "../../axis/maxAxis/maxStackAxis"
import StackLabel from "../../label/maxLabel/stackLabel"

export class StackTheme {
    constructor(
        palette= StackPalette,
        padding = StackPadding,
        axis = [
            new MaxStackAxis(AxisDirections.Left),
            new MaxStackAxis(AxisDirections.Bottom)
        ],
        label = StackLabel) {
        
        // super(palette,padding,axis,label)

        this.palette = palette
        this.padding = padding
        this.axis = axis
        this.label = label
    }

    colors(idx, stackSericeLength) {
        return this.palette.getColors(idx, stackSericeLength)
    }

    getUsedColors(arr, stackSericeLength) {
        return this.palette.usedColor(arr, stackSericeLength)
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

    axisAssist(svg, ys,ivp) {
        this.axis[0].renderBackgroundLine(svg, ys, ivp)
    }

    showLabel(svg, ivp, data) {
        const getColor = this.colors.bind(this)
        this.label.renderStackLabel(svg, ivp, data, getColor)
    }

    setXAxisTicks(min, max, n) {
        this.queryHorAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    setYAxisTicks(min, max, n) {
        this.queryVerAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    showExtraAAxis(svg, ivp) {
        this.queryHorAxis().forEach(x => x.renderExtraXAxis(svg, ivp))
    }
}

export default new StackTheme()
