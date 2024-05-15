# cxalio-studio-tools

## 介绍

这是一套用于简化影视后期工作的脚本合集。

涉及各种繁复的资料处理工作，解放双手，减少出错。

## 安装

```shell
pip --install cxalio-media-tools

#推荐使用 pipx 安装
pipx --install cxalio-media-tools
```

## 包含的工具

### MediaKiller

MediaKiller 可以通过配置文件操纵 ffmpeg 批量地对大量媒体文件转码，
仅支持单文件输入，可以保留源文件的目录层级。
请查看[具体说明](src/media_killer/help.md)

### SubConv

subconv 是一个批量从字幕文件提取台词本的工具。
请查看[具体说明](src/sub_conv/help.md)

### update_githubhosts

一个自动更新hosts的小工具

## To-do

- media-inspector 解析媒体信息

## Change-log

### 0.2.2
mediakiller:

- 修复了 duration 无法解析时崩溃的 bug。
- 修复了目标目录解析为当前目录的错误。
- 增加了扩展名检查，强制生成的配置文件扩展名为`toml`。

### 0.2.0

重新构建现有工具。

#### MediaKiller

- 增加了标签替换系统
- 增加了任务模块，统一转码和脚本生成功能
- 修改配置文件，分开输入和输出两部分，并且`input`和`output`现在是表数组了。这样就支持了多个文件的输入和输出。
- 大幅优化内存占用和性能
- 大幅调整调试信息

