import {BarCharts} from "../../histogram/charts/barcharts"
import {Histogram} from "../../histogram/histogram"
import defaultTheme from "../../histogram/theme/theme"
import defaultBubbleTheme from "../../histogram/theme/maxTheme/bubbleTheme"
import defaultPieTheme from "../../histogram/theme/pietheme"
import {MemoryDatasource} from "../../histogram/data/source/memdatasource"
import {MeasureArrayAdapter} from "../../histogram/data/adapter/measurearrayadapter"
import {BandScale} from "../../histogram/scale/band"
import {LinearScale} from "../../histogram/scale/linear"
import {LineCharts} from "../../histogram/charts/linecharts"
import {CircleCharts} from "../../histogram/charts/circlecharts"
import {PieCharts} from "../../histogram/charts/piecharts"
import {MaxCircleCharts} from "../../histogram/charts/maxCharts/maxCircleCharts";
import { MaxHistogram } from "../../histogram/maxHistogram/maxHistogram";

class MaxReportFactory {
    createHistogram(hid, dataset, fn = this.createArrayAdapter,
                    theme = defaultBubbleTheme,
                    scales= { x: new LinearScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxHistogram(hid, adapter, theme, [], scales)
    }
    createHistogramWithOutAxis(hid, dataset, fn = this.createArrayAdapter,
                    theme = defaultTheme) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxHistogram(hid, adapter, theme, [], {})
    }
    createBarCharts(dataset, fn,
                    theme = defaultTheme,
                    scales = { x: new BandScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new BarCharts(adapter, theme, scales)
    }
    createLineCharts(dataset, fn,
                     theme = defaultTheme,
                     scales = { x: new LinearScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new LineCharts(adapter, theme, scales)
    }
    createCircleCharts(dataset, fn,
                     theme = defaultBubbleTheme,
                     scales = {
                         x: new LinearScale(),
                         y: new LinearScale(),
                         r: new LinearScale() }) {

        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxCircleCharts(adapter, theme, scales)
    }
    createPieCharts(dataset, fn,
                    theme = defaultPieTheme) {

        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new PieCharts(adapter, theme)
    }
    createArrayAdapter(source) {
        return new MeasureArrayAdapter(source)
    }
}

export default new MaxReportFactory()
