
import BarLinePalette from "../property/max/barLinePalette"
import StackPadding from "../property/max/stackPadding"
import {Position} from "../utils/position"
import {MaxBarLineAxis, AxisDirections} from "../../axis/maxAxis/maxBarLineAxis"
import BarLineLabel from "../../label/maxLabel/barLineLabel"
import { timeWednesday } from "d3"

export class StackTheme {
    constructor(
        palette= BarLinePalette,
        padding = StackPadding,
        axis = [
            new MaxBarLineAxis(AxisDirections.Left),
            new MaxBarLineAxis(AxisDirections.Bottom),
            new MaxBarLineAxis(AxisDirections.Right)
        ],
        label = BarLineLabel) {
        
        // super(palette,padding,axis,label)

        this.palette = palette
        this.padding = padding
        this.axis = axis
        this.label = label
    }

    colors(idx) {
        return this.palette.getColors(idx)
    }

    getUsedColors() {
        return this.palette.usedColor()
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
                result.h -= it.axisWidth()
            } else if (it.isLeft()) {
                result.x += it.axisWidth() + 60 
            } else if (it.isRight()) {
                result.w -=  it.axisWidth() + 60
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
        const resultLeft = new Position(pos.x, pos.y, 0, pos.h)
        const resultRight = new Position(pos.x, pos.y, pos.w, pos.h)
        const resultBottom = new Position(pos.x, pos.y, pos.w, 0)
        
        
        if (info) {
            
            // 坐标的处理
            if (info["bottomTitle"]) {
                resultBottom.h += 40
            }
            if (info["labels"]) {
                // labels：有几行图例 
                const lh = info["labels"] * 40
                resultBottom.y = temp.y + temp.h - lh
                resultBottom.h += lh
            } 
            if (info["leftTitle"]) {
                resultLeft.w = 40
                resultLeft.h = temp.h - resultBottom.h 
            } 
            if (info["rightTitle"]) {
                resultRight.x = temp.x + temp.w
                resultRight.w = 40
                resultRight.h = temp.h - resultBottom.h 
            }            
        }
        return {
            left: resultLeft,
            right: resultRight,
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

    showLabel(svg, ivpInfo, data) {
        const colors = this.getUsedColors()
        this.label.renderBarLineLabel(svg, ivpInfo, data, colors)
    }

    setXAxisTicks(min, max, n) {
        this.queryHorAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    setYAxisTicks(min, max, n) {
        this.queryVerAxis().forEach(x => x.getAxisTicks(min, max, n))
    }

    showExtraAAxis(svg, ys,ivp) {
        this.queryHorAxis().forEach(x => x.renderExtraXAxis(svg, ys,ivp))
    }

    showTitle(ivpInfo, svg, titleObject) {
        if (titleObject.right) {
            this.axis[0].showRightTitle(svg, titleObject.right, ivpInfo)
        }
        
        if (titleObject.left) {
            this.axis[0].showLeftTitle(svg, titleObject.left, ivpInfo)
        }
    }
}

export default new StackTheme()
