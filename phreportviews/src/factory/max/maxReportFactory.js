import defaultTheme from "../../histogram/theme/theme"
import defaultBubbleTheme from "../../histogram/theme/maxTheme/bubbleTheme"
import defaultStackTheme from "../../histogram/theme/maxTheme/stackTheme"
import defaultBarLineTheme from "../../histogram/theme/maxTheme/barLineTheme"
import defaultPieTheme from "../../histogram/theme/pietheme"
import {MemoryDatasource} from "../../histogram/data/source/memdatasource"
import {MeasureArrayAdapter} from "../../histogram/data/adapter/measurearrayadapter"
import {TimeScale} from "../../histogram/scale/time"
import {LinearScale} from "../../histogram/scale/linear"
import {PieCharts} from "../../histogram/charts/piecharts"
import {MaxCircleCharts} from "../../histogram/charts/maxCharts/maxCircleCharts";
import {MaxStackCharts} from "../../histogram/charts/maxCharts/maxStackCharts";
import {MaxBarCharts} from "../../histogram/charts/maxCharts/maxBarCharts";
import {MaxLineCharts} from "../../histogram/charts/maxCharts/maxLineCharts";
import { MaxBubbleHistogram } from "../../histogram/maxHistogram/maxBubbleHistogram";
import { MaxStackHistogram } from "../../histogram/maxHistogram/maxStackHistogram";
import { MaxBarLineHistogram } from "../../histogram/maxHistogram/maxBarLineHistogram";

class MaxReportFactory {
    // bubble 需要改名处理
    createBubbleHistogram(hid, dataset, fn = this.createArrayAdapter,
                    theme = defaultBubbleTheme,
                    scales= { x: new LinearScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxBubbleHistogram(hid, adapter, theme, [], scales)
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
    
    // stack
    createStackHistogram(hid, dataset, fn = this.createArrayAdapter,
        theme = defaultStackTheme,
        scales= { x: new TimeScale(), y: new LinearScale() }) {
            const source = new MemoryDatasource(dataset)
            const adapter = fn(source)
            return new MaxStackHistogram(hid, adapter, theme, [], scales)
    } 
    createStackCharts(dataset, fn,
        theme = defaultStackTheme,
        scales = { x: new TimeScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxStackCharts(adapter, theme, scales)
    }

    // bar-line 
    createBarLineHistogram(hid, dataset, fn = this.createArrayAdapter,
        theme = defaultBarLineTheme,
        scales= { x: new TimeScale(), y: new LinearScale(), yRight: new LinearScale() }) {
            const source = new MemoryDatasource(dataset)
            const adapter = fn(source)
            return new MaxBarLineHistogram(hid, adapter, theme, [], scales)
    } 

    createBarCharts(dataset, fn,
        theme = defaultBarLineTheme,
        scales = { x: new TimeScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxBarCharts(adapter, theme, scales)
    }


    createLineCharts(dataset, fn,
                     theme = defaultBarLineTheme,
                     scales = { x: new TimeScale(), y: new LinearScale() }) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxLineCharts(adapter, theme, scales)
    }

    createHistogramWithOutAxis(hid, dataset, fn = this.createArrayAdapter,
        theme = defaultTheme) {
        const source = new MemoryDatasource(dataset)
        const adapter = fn(source)
        return new MaxHistogram(hid, adapter, theme, [], {})
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
