import {Position} from "../theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "../scale/linear"
import {BandScale} from "../scale/band"
import {TimeScale} from "../scale/time"
import { Histogram } from "../histogram"
import label from "../label/defaultlabel"

export class MaxStackHistogram extends Histogram {
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
                domain: [0, this.source.max() * 1.1], // 叠加后的最大值
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
        const labelData = this.source.keys().length
        const labelLines = labelData % 4 === 0 ? labelData / 4 : Math.floor(labelData / 4) + 1 
        const vp = this.theme.histogramRect(new Position(0, 0, width, height))
        const infoObj = {
            "leftTitle": yTitle,
            "rightTitle": undefined,
            "bottomTitle": undefined,
            "labels": labelLines
        }
        const ivp = this.theme.histogramInnerRect(vp, infoObj)
        const ivpInfo = this.theme.histogramOuterInfo(vp, infoObj)

        // 图表
        const svg = d3.select(this.hid)
                .append("svg")
                .attr("width", width)
                .attr("height", height)

        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)
    
        this.theme.setYAxisTicks(0, this.source.max() * 1.1, 3)
        this.theme.axisAssist(svg, yAxisScale,ivp)
            
        this.charts.forEach(x => x.render(svg, ivp))
        
        this.theme.showExtraAAxis(svg, ivp)
        this.theme.showLabel(svg, ivpInfo, this.source.keys())

        if (xAxisScale) {
            this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        }

        if (yAxisScale) {
            this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))
        }

        if (xTitle) {
            this.theme.queryHorAxis().forEach(x => x.showXTitle(svg, xTitle, ivpInfo))
        }

        if (yTitle) {
            this.theme.queryVerAxis().forEach(x => x.showYTitle(svg, yTitle, ivpInfo))
        }
    }

    registerCharts(c) {
        this.charts.push(c)
    }
}
