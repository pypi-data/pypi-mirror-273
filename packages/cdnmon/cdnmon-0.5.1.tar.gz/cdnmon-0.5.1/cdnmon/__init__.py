import glob
import importlib
import os

from cdnmon.model.cdn import CommonCDN


def CDN(name: str) -> CommonCDN:
    module_name = f"cdnmon.model.cdn.{name.replace('-', '_')}"
    module = importlib.import_module(module_name)
    return module.CDN


__all__ = ["CDN"]


def main():
    for path in glob.glob(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "*.yaml")):
        cdn_name, _ = os.path.splitext(os.path.basename(path))
        cdn = CDN(cdn_name)
        print(cdn)


if __name__ == "__main__":
    main()
