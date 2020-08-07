import {Position} from "../theme/utils/position"
import * as d3 from "d3"
import {LinearScale} from "../scale/linear"
import { Histogram } from "../histogram";

export class MaxHistogram extends Histogram {
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
        console.log("this.source.max()", this.source.max())
        const x = this.scales["x"]
        if (x) {
            const opt = {
                domain: [this.source.min()[0]*0.9, this.source.max()[0]*1.1],
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
                domain: [this.source.min()[1]*0.9, this.source.max()[1]*1.1],
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
        const ivp = this.theme.histogramInnerRect(vp)
        const svg = d3.select(this.hid)
            .append("svg")
            .attr("width", width)
            .attr("height", height)

        const xAxisScale = this.genXAxisScale(ivp)
        const yAxisScale = this.genYAxisScale(ivp)

        this.theme.axisAssist(svg, ivp)
        this.theme.showLabel(svg, ivp)
        this.theme.setXAxisTicks(this.source.min()[0] * 0.9, this.source.max()[0]*1.1, 5)
        this.theme.setYAxisTicks(this.source.min()[1] * 0.9, this.source.max()[1]*1.1, 3)
        this.theme.createColors(svg)
        this.theme.clipBubbleChart(svg, ivp)

        this.charts.forEach(x => x.render(svg, ivp))

        if (xAxisScale) {
            this.theme.queryHorAxis().forEach(x => x.render(svg, xAxisScale, ivp))
        }

        // if (yAxisScale) {
        //     this.theme.queryVerAxis().forEach(x => x.render(svg, yAxisScale, ivp))
        // }

        this.showTitle(ivp,svg, xTitle, yTitle)
    }

    registerCharts(c) {
        this.charts.push(c)
    }

    showTitle(ivp,svg, xTitle, yTitle) {
        if (xTitle) {
            this.theme.queryHorAxis().forEach(x => x.showXTitle(svg, xTitle, ivp))
        }

        if (yTitle) {
            this.theme.queryVerAxis().forEach(x => x.showYTitle(svg, yTitle, ivp))
        }
    }
}
