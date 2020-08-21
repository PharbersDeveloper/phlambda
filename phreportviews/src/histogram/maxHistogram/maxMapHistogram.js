import {Position} from "../theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "../scale/linear"
import { Histogram } from "../histogram";

export class MaxMapHistogram extends Histogram {
    constructor(
        hid,
        source,
        theme,
        charts = [],
        scales = { x : new LinearScale(), y: new LinearScale() }) {

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
                domain: [0,1],
                rangeRound: [ivp.x, ivp.w],
                paddingInner: 0.05
            }
            return x.genScale(opt)
        } else return null
    }

    genYAxisScale(ivp) {
        const y = this.scales["y"]
        if (y) {
            const opt = {
                domain: [0,1],
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
    render(width, height, xTitle, yTitle) {
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const infoObj = {
            "leftTitle": xTitle,
            "rightTitle": undefined,
            "bottomTitle": undefined,
            "labels": undefined
        }
        const ivp = this.theme.histogramInnerRect(vp, infoObj)
        const ivpInfo = this.theme.histogramOuterInfo(vp, infoObj)
        const svg = d3.select(this.hid)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
        

        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)

        // 展示图例等信息
        this.theme.showLabel(svg, ivpInfo, { min: this.source.min(), max: this.source.max() })


        this.charts.forEach(x => x.render(svg, ivp))
    }

    registerCharts(c) {
        this.charts.push(c)
    }
}
