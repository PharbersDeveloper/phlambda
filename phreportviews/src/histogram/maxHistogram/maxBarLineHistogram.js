import {Position} from "../theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "../scale/linear"
import {TimeScale} from "../scale/time"
import { Histogram } from "../histogram"
import label from "../label/defaultlabel"

export class MaxBarLineHistogram extends Histogram {
    constructor(
        hid,
        source,
        theme,
        charts = [],
        scales = { x : new TimeScale(), y: new LinearScale() }) {

        super(hid, source, theme, charts, scales)

        this.hid = hid
        this.theme = theme
        this.source = source
        this.charts = charts
        this.scales = scales
    }

    genXAxisScale(ivp) {
        const x = this.scales["x"]
        if (x) {
            const opt = {
                domain: [new Date("2018-01"), new Date("2019-12")],
                rangeRound: [ivp.x,  ivp.w],
                paddingInner: 0.05
            }
            return x.genScale(opt)
        } else return null
    }

    genYAxisScale(ivp) {
        const y = this.scales["y"]
        const yMax = d3.max(this.source.max())
        if (y) {
            const opt = {
                domain: [0, yMax],
                rangeRound: [ivp.h, ivp.y]
            }
            return y.genScale(opt)
        } else return null
    }

    genYAxisScaleRight(ivp) {
        const y = this.scales["yRight"]
        if (y) {
            const opt = {
                domain: [-1, 1],
                rangeRound: [ivp.h, ivp.y]
            }
            return y.genScale(opt)
        } else return null
    }

    displayHistogram(width, height, xTitle, yTitle) {
        this.render(width, height, xTitle, yTitle)
        // this.events()
    }

  

    /**
     * 3. Render the initial view
     */
    render(width, height, rightTitle, leftTitle) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const infoObj = {
            "leftTitle": leftTitle,
            "rightTitle": rightTitle,
            "bottomTitle": undefined,
            "labels": 1
        }
        const ivp = this.theme.histogramInnerRect(vp, infoObj)
        const ivpInfo = this.theme.histogramOuterInfo(vp, infoObj)
        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)
        const yAxisScaleRight = this.genYAxisScaleRight(ivp)

        // 图表
        const svg = d3.select(this.hid)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            
            
        
        const yMax = d3.max(this.source.max())
        this.theme.setYAxisTicks(0, yMax, 4)
        this.theme.axisAssist(svg, yAxisScale,ivp)
            
        this.charts.forEach(x => x.render(svg, ivp))
        
        this.theme.showExtraAAxis(svg, yAxisScale,ivp)
        
        this.theme.showLabel(svg, ivpInfo, this.source.keys())

        if (xAxisScale) {
            this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        }

        // 双y轴处理
        if (yAxisScale || yAxisScaleRight) {
            this.theme.queryVerAxis().forEach(x => {
                if (x.isRight()) {
                    x.render(svg, yAxisScaleRight, ivp)
                } 

                if (x.isLeft()) {
                    x.render(svg, yAxisScale, ivp)
                }
            })
        }
        this.theme.showTitle(ivpInfo, svg, {right: rightTitle, left: leftTitle})
        
    }

    registerCharts(c) {
        this.charts.push(c)
    }
}
