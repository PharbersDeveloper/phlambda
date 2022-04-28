# 各个lambda的描述，基于Dictiory

## data 

- 用于外部数据，比如广网等

## deprecated

- 用于以前有用，现在已经不在维护的代码

## lambdas 是所有现有无服务化函数的

- 以后lambdas全部以流程为核心
- 分为同步消息和异步消息
- 同步函数全部走Http （API Gateway）
- 异步全部走Step Function 调度Lambda，不要消息了 学习太难

如上描述，

```
-- phlambda
 |-- data                       # 外部需要保存的数据
 |-- deprecated                 # 不在维护的代码
  ｜-- ...                         # 其内部结构参考processor
 |-- layer                      # lambda layer
 |-- processor                  # 所有正在使用，并持续维护的lambda
  ｜-- sync                        # 同步的lambda
    ｜-- <function-name>              # 函数名称
      ｜-- src                           # 代码
      ｜-- test                          # 单元测试代码
      ｜-- buildspec.yaml                # 编译配置
      ｜-- template.yaml                 # 部署配置
  ｜-- async                       # 异步的lambda
    ｜-- <process-name>               # 流程名称
      ｜-- steps.yaml                    # 流程详细化描述
      ｜-- <function-name>               # 函数名称
        ｜-- src                           # 代码
        ｜-- test                          # 单元测试代码
        ｜-- buildspec.yaml                # 编译配置
        ｜-- template.yaml                 # 部署配置
 ｜-- devops
   ｜-- <process-name>               # 流程名称
      ｜-- steps.yaml                    # 流程详细化描述
      ｜-- <function-name>               # 函数名称
        ｜-- src                           # 代码
        ｜-- test                          # 单元测试代码
        ｜-- buildspec.yaml                # 编译配置
        ｜-- template.yaml                 # 部署配置
```