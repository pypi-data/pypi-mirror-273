#!python3
###
### 配置默认使用 config.toml  
### 
import argparse
import os
# import json
# import rtoml
import sys

from pprint import pprint, pformat

_curdir = os.path.abspath(os.path.dirname(__file__))
_srcdir = os.path.dirname(_curdir)
if _srcdir not in sys.path:
    sys.path.insert(0, _srcdir)

# pprint(sys.path, indent=2)
import webhook_cli
from webhook_cli.ext.dingtalk import WebhookDingTalk


def main():
    """
    --help              ; 显示参数列表
    --version           ; 获取版本号
    --config            ; 显示默认的配置文件， 及其内容
    """
    PROG = "webhook"
    if sys.argv[0].startswith("."):
        PROG = sys.argv[0]
    tip_help = f"如需帮助，请运行: {PROG} --help"
    tip_usage = webhook_cli.long_usage + os.linesep + os.path.abspath(__file__) + os.linesep
    # tip_usage = webhook_cli.long_usage + os.linesep * 2 + WebhookDingTalk.desc
    sys_parser = argparse.ArgumentParser(usage=tip_usage, prog=PROG)
    sys_parser.add_argument("-v", "--version", help="显示版本号", action="store_true")
    sys_parser.add_argument("-d", "--dry_run", help="不运行，只打印调试参数", action="store_true")
    sys_parser.add_argument("-i", "--init_config", help="生成默认配置(./config.toml)", action="store_true")
    sys_parser.add_argument("-c", "--check_config", help="检查当前的配置", action="store_true")
    sys_parser.add_argument("--webhook_url", help="如果设定，将覆盖默认配置的webhook_url", default="")
    sys_parser.add_argument("--file", help="必须是可读的文本文件，支持markdown文件(.md);\n"
                                           "\t如果是toml/json，将按照`msgtype`转发；\n"
                                           "\t如果不可识别`msgtype`, 使用raw模式", default=""
                            )
    sys_parser.add_argument("--mode",
                            help="[发送模式]默认为auto,如果json/toml内没有指定 msgtype, 则把文件内容序列化；如果设置为raw, 则把$file视为text的内容；",
                            default="auto"
                            )

    # sys_args = sys_parser.parse_intermixed_args()
    sys_args, _unknown_argv = sys_parser.parse_known_args()
    if sys_args.version:
        # print(f"version: {webhook_cli.__version__}", sys_args.version)
        print(f"version: {webhook_cli.__version__} ({__file__})")
        return 0

    if not sys_args.file:
        if len(_unknown_argv) > 0:
            sys_args.file = _unknown_argv[-1]

    if sys_args.dry_run:
        pprint(sys_args, indent=2)
        print("_unknown_:", pformat(_unknown_argv, indent=2), type(_unknown_argv))
        return 0

    if sys_args.check_config:
        WebhookDingTalk.get_config_options(stdout=True)
        return 0

    if sys_args.init_config:
        WebhookDingTalk.set_config_sample()
        return 0

    config_options = {}
    if sys_args.webhook_url:
        config_options["mode"] = sys_args.mode
        config_options["webhook_url"] = sys_args.webhook_url

    print("[发送模式]", sys_args.mode)
    if sys_args.mode == "raw":
        _unknown_argv.insert(0, config_options.get("keyword", "[测试通知-raw]"))
        text = " ".join(_unknown_argv)
        if not os.path.isfile(sys_args.file):
            if sys_args.file not in _unknown_argv[-2:]:
                text += f"\n{sys_args.file}"
        else:
            with open(sys_args.file, "r") as fr:
                content = fr.read()
            text += f"\n\n{content}\n"

        code, resp = WebhookDingTalk.send_text(text, **config_options)
        return code

    if not os.path.isfile(sys_args.file):
        print(f"[参数异常] 请提供文本文件$file(通知的内容), 支持文件(txt/md/json/toml)。")
        print(f"[无效参数] --file={sys_args.file}\n")
        print(tip_help)
        return -2
    else:
        code = WebhookDingTalk.send_file(sys_args.file, **config_options)
        return code


if __name__ == '__main__':
    main()
