
import MapPalette from "../property/max/mapPalette"
import StackPadding from "../property/max/stackPadding"
import {Position} from "../utils/position"
import {MaxMapAxis, AxisDirections} from "../../axis/maxAxis/maxMapAxis"
import MapLabel from "../../label/maxLabel/mapLabel"
import { timeWednesday } from "d3"

export class MapTheme {
    constructor(
        palette= MapPalette,
        padding = StackPadding,
        axis = [
            new MaxMapAxis(AxisDirections.Left),
            new MaxMapAxis(AxisDirections.Bottom),
        ],
        label = MapLabel) {
        
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
                result.x += it.axisWidth() 
            } else if (it.isRight()) {
                result.w -=  it.axisWidth()
            }
        })

        if (info) {
           if (info["leftTitle"]) {
                result.x += 80
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
                resultLeft.w = 80
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

    showLabel(svg, ivpInfo, data) {
        const colors = this.getUsedColors()
        this.label.renderMapLabel(svg, ivpInfo, data)
    }

}

export default new MapTheme()
