{
"common": {
"tranceId": "",
"runnerId": "sample_sample_developer_2022-07-04T05:49:39+00:00",
"projectId": "Dp10sMiAYXWxRZj",
"projectName": "sample",
"owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
"showName": "赵浩博",
"tenantId": "zudIcG_17yj8CEUoCTHg"
},
"shares": [
{
"traget": "ds name", // 共享时的目标DS 名称
"targetCat": "catalog | intermediate | uploaded", // 共享时的目标DS的类型  catalog是数据目录  intermediate是结果数据集  uploaded 是上传的数据 都需要分别处理
"sourceSelectVersions": ["version1", "version2", "version3"]
"source": "ds name", // 共享时的源DS 名称
}
]
}


做展开操作然后对比schema，源的schema与target的scheam不一致报错
都是append操作
intermediate =>
"s3://ph-platform/2020-11-11/lake/pharbers/RL8iefdfGuRfbuN/PySparkC/"
读取数据后进行多级Schema的压缩操作，写入到对应ds下面，代码都有，直接抄过来就行

catalog =>
"s3://ph-platform/2020-11-11/lake/pharbers/zudIcG_17yj8CEUoCTHg/chemdata/"
读取数据后不进行多级Schema压缩操作，写入到Catalog对应的目录下


uploaded =>
"s3://ph-platform/2020-11-11/lake/pharbers/RL8iefdfGuRfbuN/A/"
上传文件比较特殊，需要先读取DynamoDB的dataset里面的schema然后进行指定（这也有代码）
然后append数据，要输出为csv的格式