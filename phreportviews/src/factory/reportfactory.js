import {BarCharts} from "../histogram/charts/barcharts"
import {Histogram} from "../histogram/histogram"
import defaultTheme from "../histogram/theme/theme"
import {MemoryDatasource} from "../histogram/data/source/memdatasource"
import {MeasureArrayAdapter} from "../histogram/data/adapter/measurearrayadapter"
import {BandScale} from "../histogram/scale/band"
import {LinearScale} from "../histogram/scale/linear"
import {LineCharts} from "../histogram/charts/linecharts"
import {CircleCharts} from "../histogram/charts/circlecharts"

class ReportFactory {
    createHistogram(dataset, fn = this.createArrayAdapter,
                    theme = defaultTheme,
                    scales= { x: new LinearScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new Histogram(adapter, theme, [], scales)
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
                     theme = defaultTheme,
                     scales = {
                         x: new LinearScale(),
                         y: new LinearScale(),
                         r: new LinearScale() }) {

        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new CircleCharts(adapter, theme, scales)
    }
    createArrayAdapter(source) {
        return new MeasureArrayAdapter(source)
    }
}

export default new ReportFactory()
