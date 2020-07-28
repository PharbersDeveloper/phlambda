import {BarCharts} from "../histogram/charts/barcharts"
// import {Theme} from "../histogram/theme/theme"
import defaultTheme from "../histogram/theme/theme"
import {MemoryDatasource} from "../histogram/data/source/memdatasource"

class ReportFactory {
    createHistogram() {
        return new BarCharts(
            new MemoryDatasource([1,2,3,4,5]),
            defaultTheme
        )
    }
}

export default new ReportFactory()
