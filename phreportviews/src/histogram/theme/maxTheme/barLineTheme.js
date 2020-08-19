
import BarLinePalette from "../property/max/barLinePalette"
import StackPadding from "../property/max/stackPadding"
import {Position} from "../utils/position"
import {MaxBarLineAxis, AxisDirections} from "../../axis/maxAxis/maxBarLineAxis"
import BarLineLabel from "../../label/maxLabel/barLineLabel"

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
                result.h -= it.axisWidth() + 40
            } else if (it.isLeft()) {
                result.x += it.axisWidth() + 40
            } else if (it.isRight()) {
                // result.w = 950
                console.log("axisWidth", it.axisWidth())
                result.w -= 80
            }
        })

        if (info) {
           if (info["leftTitle"]) {
                result.x += 40
           } else if (info["rightTitle"]) {
                result.w -= 40
           } else if (info["bottomTitle"]) {
                result.h -= 40
           } else if (info["labels"]) {
               // labels：有几行图例 
                result.h -= info["labels"] * 40
           }
        }
        
        return result
    }

    histogramOuterInfo(pos, info) {
        const resultLeft = new Position(pos.x, pos.y, pos.w, pos.h)
        const resultRight = new Position(pos.x, pos.y, pos.w, pos.h)
        const resultBottom = new Position(pos.x, pos.y, pos.w, pos.h)
        
        
        if (info) {
            
            // 坐标的处理
            if (info["bottomTitle"]) {
                resultBottom.h = 40
            }
            if (info["labels"]) {
                resultBottom.y += resultBottom.h - info["labels"] * 40
                
                // labels：有几行图例 
                const lh = info["labels"] * 40
                resultBottom.h = lh
            } 
            if (!info["bottomTitle"] && !info["labels"]) {
                resultBottom.h = 0
            }
            if (info["leftTitle"]) {
                resultLeft.w = 40
                resultLeft.h -= resultBottom.h 
            } 
            if (info["rightTitle"]) {
                resultRight.x += resultRight.w
                resultRight.w = 40
                resultRight.h -= resultBottom.h 
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
        console.log("kokodayo2", ivpInfo)
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
            svg.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(${ivpInfo.right.x + ivpInfo.right.w / 2 }, ${ivpInfo.right.h / 2}) rotate(270, 10 10)`)
                .text(titleObject.right)   
        }
            
        if (titleObject.left) {
            svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpInfo.left.w/2 }, ${ivpInfo.left.h / 2}) rotate(270, 10 10)`)
            .text(titleObject.left)
        }
    }
}

export default new StackTheme()
