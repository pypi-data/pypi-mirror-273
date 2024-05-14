import os


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OK = WARNING


def env_bool(k: str, default=False):
    v = os.environ.get(k, None)
    vf = ["n", "no", "false", "0", "disabled", "disable", "否"]
    vt = ["y", "yes", "true", "1", "enabled", "enable", "是"]
    if str(v).lower() in vt:
        return True
    if str(v).lower() in vf:
        return False
    return default


def env(k: str, default="", nullable=False):
    v = os.environ.get(k, None)
    if v is None:
        print(f"[env]: unset ${k}, default={default}")
        return default
    elif v == "" and not nullable:
        v = default
    print(f"[env]: get ${k}={default}")
    return v
