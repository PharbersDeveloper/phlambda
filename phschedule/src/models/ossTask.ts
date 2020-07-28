"use strict"
import {JsonObject, JsonProperty} from "json2typescript"

@JsonObject("OssTask")
export class OssTask {

    @JsonProperty("AssetId", String)
    public assetId: string = undefined

    @JsonProperty("JobId", String)
    public jobId: string = undefined

    @JsonProperty("TraceId", String)
    public traceId: string = undefined

    @JsonProperty("OssKey", String)
    public ossKey: string = undefined

    @JsonProperty("FileType", String)
    public fileType: string = undefined

    @JsonProperty("FileName", String)
    public fileName: string = undefined

    @JsonProperty("SheetName", String)
    public sheetName: string = undefined

    @JsonProperty("Owner", String)
    public owner: string = undefined

    @JsonProperty("CreateTime", Number)
    public createTime: number = undefined

    @JsonProperty("Labels", [String])
    public labels: string[] = undefined

    @JsonProperty("DataCover", [String])
    public dataCover: string[] = undefined

    @JsonProperty("GeoCover", [String])
    public geoCover: string[] = undefined

    @JsonProperty("Markets", [String])
    public markets: string[] = undefined

    @JsonProperty("Molecules", [String])
    public molecules: string[] = undefined

    @JsonProperty("Providers", [String])
    public providers: string[] = undefined
}
