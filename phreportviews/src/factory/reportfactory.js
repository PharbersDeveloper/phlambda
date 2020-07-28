import {BarCharts} from "../histogram/charts/barcharts"
import {Histogram} from "../histogram/histogram"
import defaultTheme from "../histogram/theme/theme"
import {MemoryDatasource} from "../histogram/data/source/memdatasource"
import {MeasureArrayAdapter} from "../histogram/data/adapter/measurearrayadapter"

class ReportFactory {
    createBarChart() {
        const source = new MemoryDatasource([1,2,3,4,5])
        const adapter = new MeasureArrayAdapter(source)
        return new Histogram(
            adapter,
            defaultTheme,
            [new BarCharts(adapter, defaultTheme)]
        )
    }
}

export default new ReportFactory()
