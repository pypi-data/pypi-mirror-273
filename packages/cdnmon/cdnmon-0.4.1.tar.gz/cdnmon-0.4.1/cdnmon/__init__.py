import functools
import glob
import logging
import os

import coloredlogs
import requests
import yaml

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


class CDN:
    def __init__(self, name):
        self._data = self._fetch_cdn_data(name)
        self.name = self._data["name"]
        self.cname_suffixes = self._data["cname_suffixes"] if "cname_suffixes" in self._data.keys() else []
        self.asn_patterns = self._data["asn_patterns"] if "asn_patterns" in self._data.keys() else []
        self.ipv4_prefixes = self._data["ipv4_prefixes"] if "ipv4_prefixes" in self._data.keys() else []
        self.ipv6_prefixes = self._data["ipv6_prefixes"] if "ipv6_prefixes" in self._data.keys() else []
        self.updated_at = self._data["updated_at"] if "updated_at" in self._data.keys() else ""

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _fetch_cdn_data(name):
        url = f"https://cdnmon.vercel.app/{name}.yaml"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch CDN data from {url}, status code: {response.status_code}")
        return yaml.safe_load(response.content)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


__all__ = ["CDN"]


def main():
    for path in glob.glob(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "*.yaml")):
        cdn_name, _ = os.path.splitext(os.path.basename(path))
        cdn = CDN(cdn_name)
        print(cdn)


if __name__ == "__main__":
    main()
