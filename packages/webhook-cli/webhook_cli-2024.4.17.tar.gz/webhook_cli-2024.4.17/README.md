# Webhook Cli

- webhook通知-命令行工具(v2023.3.14)

-----

## 支持
- [x] dingtalk (钉钉群机器人)
  - [x] 支持文本 (text)
  - [x] 支持链接 (link)
  - [x] 支持 markdown(markdown)
  - [x] 支持 ActionCard
  - [x] 支持 FeedCard消息类型
- [ ] gitlab
- [ ] coding.net
- [ ] feishu

## 安装：

- pip install webhook-cli

## 功能设计：

```text
> webhook --help

usage: webhook命令行工具 ({__version__})
eg:
  [0] webhook --init_config        ; 初始化配置模板 
  [1] webhook --check_config       ; 检查配置   
  [2] webhook msg.txt              ; text 发送   
  [3] webhook msg.md               ; markdown 发送 
  [4] webhook msg.toml             ; 支持 toml    
  [5] webhook msg.json             ; 支持 json5
  [6] webhook --file msg.json      ; 支持使用形参 --file, 效果同[5], 提高容错
  
  [7] webhook msg.toml --webhook_url https://oapi.dingtalk.com/robot/send?access_token= 
  [8] webhook --webhook_url https://oapi.dingtalk.com/robot/send?access_token= msg.toml 
    ; 效果同[6]，提高容错 

## 配置优先级(从高到低往下排)：
    0.  --file(toml/json)内置的 options.webhook_url
    1.  --webhook_url 
    2.  进程环境的配置文件( ENV.$WEBHOOK_CONFIG  ) 
    3.  当前工作目录下的 config.toml  
    4.  Ubuntu系统全局默认：$HOME/.config/webhook_cli/config.toml 


## 可选参数
options:
  -h, --help                  ; show this help message and exit
  -v, --version               ; 显示版本号
  -d, --dry_run               ; 不运行，只打印调试参数
  -i, --init_config           ; 生成默认配置(./config.toml)
  -c, --check_config          ; 检查当前的配置
  --webhook_url WEBHOOK_URL   ; 如果设定，将覆盖默认配置的webhook_url
                              
  --file FILE                 ; 必须是可读的文本文件，支持markdown文件(.md); 
                              如果是toml/json，将按照`msgtype`转发； 
                              如果不可识别`msgtype`, 使用raw模式
                              
  --mode MODE                 ; 指定发送模式；如果设置为raw, 则把$file视为text的内容; 
                              默认为auto,如果json/toml内没有指定 msgtype, 则把文件内容序列化

``` 

## 常见的发送错误

```json lines
// 消息内容中不包含任何关键词
{
  "errcode": 310000,
  "errmsg": "keywords not in content"
}

// timestamp 无效
{
  "errcode": 310000,
  "errmsg": "invalid timestamp"
}

// 签名不匹配
{
  "errcode": 310000,
  "errmsg": "sign not match"
}

// IP地址不在白名单
{
  "errcode": 310000,
  "errmsg": "ip X.X.X.X not in whitelist"
}
```