
import StackPalette from "../property/max/StackPalette"
import Theme from "../theme"
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

    getUsedColors(arr) {
        return this.palette.usedColor(arr)
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
    histogramInnerRect(pos, info) {
        const result = new Position(pos.x, pos.y, pos.w, pos.h)
        this.axis.forEach((it) => {
            if (it.isUp()) {
                result.y += it.axisWidth()
            } else if (it.isBottom()) {
                result.h -= it.axisWidth() + 20
            } else if (it.isLeft()) {
                result.x += it.axisWidth() + 60
            } else if (it.isRight()) {
                result.w -= it.axisWidth()
            }
        })

        if (info) {
            if (info["leftTitle"]) {
                 result.x += 40
            } 
            if (info["rightTitle"]) {
                 result.w -= 40
            } 
            if (info["bottomTitle"]) {
                 result.h -= 40
            } 
            if (info["labels"]) {
                // labels：有几行图例 
                result.h -= info["labels"] * 24
            }
         }
        return result
    }

    histogramOuterInfo(pos, info) {
        const temp = new Position(pos.x, pos.y, pos.w, pos.h)        
        const resultLeft = new Position(pos.x, pos.y, pos.w, pos.h)        
        const resultBottom = new Position(pos.x, pos.y, pos.w, pos.h)        
        
        if (info) {
            
            // 坐标的处理
            if (info["labels"]) {
                // labels：有几行图例 
                const lh = info["labels"] * 24
                resultBottom.h = lh
                resultBottom.y = temp.y + temp.h - lh
            } 

            if (info["leftTitle"]) {
                resultLeft.w = 40
                resultLeft.h = temp.h - resultBottom.h 
            }  
        }
        return {
            left: resultLeft,
            bottom: resultBottom
        }

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

    showLabel(svg, ivpinfo, data) {
        const getColor = this.getUsedColors(data)
        this.label.renderStackLabel(svg, ivpinfo, data, getColor)
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
