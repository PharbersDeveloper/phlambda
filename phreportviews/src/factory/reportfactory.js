import {BarCharts} from "../histogram/charts/barcharts"
import {Histogram} from "../histogram/histogram"
import defaultTheme from "../histogram/theme/theme"
import {MemoryDatasource} from "../histogram/data/source/memdatasource"
import {MeasureArrayAdapter} from "../histogram/data/adapter/measurearrayadapter"

class ReportFactory {
    createHistogram(dataset, fn, theme = defaultTheme) {
        const source = new MemoryDatasource(dataset)
        // const adapter = new MeasureArrayAdapter(source)
        const adapter = fn(source)
        return new Histogram(
            adapter,
            theme, []
            // [new BarCharts(adapter, defaultTheme)]
        )
    }
    createBarCharts(dataset, fn, theme = defaultTheme) {
        const source = new MemoryDatasource(dataset)
        // const adapter = new MeasureArrayAdapter(source)
        const adapter = fn(source)
        return new BarCharts(
            adapter,
            theme
        )
    }
    // registerCharts(h, c) {
    //     h.registerCharts(c)
    // }
    createArrayAdapter(source) {
        return new MeasureArrayAdapter(source)
    }
}

export default new ReportFactory()
