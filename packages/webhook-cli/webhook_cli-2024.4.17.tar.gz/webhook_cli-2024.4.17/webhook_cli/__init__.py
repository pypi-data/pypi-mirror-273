"""
    webhook-cli
    ~~~~~~~~~~

    webhook-cli msg.json
    webhook-cli --url

    :copyright: © 2023 by the NicoNing.
    :license: GPL, see LICENSE for more details.
"""

__version__ = '2024.4.17'

long_usage = f"""
    
    webhook命令行工具 ({__version__})

eg:
  [0] webhook --init_config        ; 初始化配置模板 
  [1] webhook --check_config       ; 检查配置   
  [2] webhook msg.txt              ; text发送   
  [3] webhook msg.md               ; markdown发送 
  [4] webhook msg.toml             ; 支持 toml    
  [5] webhook msg.json             ; 支持 json5
  [6] webhook --file msg.json      ; 支持使用形参 --file
  [6] webhook msg.json --mode raw  ; 使用raw模式，读取文件文本，text发送
  
  [8] webhook msg.toml --webhook_url https://oapi.dingtalk.com/robot/send?access_token= 
  [9] webhook --webhook_url https://oapi.dingtalk.com/robot/send?access_token= msg.toml 
      ; 效果同[8]，提高容错 

## 配置优先级(从高到低往下排)：
  [0] --file(toml/json)内置的 options.webhook_url
  [1] --webhook_url 
  [2] 当前进程，使用环境变量指定的配置文件(ENV.$WEBHOOK_CONFIG) 
  [4] 当前工作目录下的 config.toml  
  [5] Ubuntu系统全局默认：$HOME/.config/webhook_cli/config.toml 

## 可选参数:   
"""

