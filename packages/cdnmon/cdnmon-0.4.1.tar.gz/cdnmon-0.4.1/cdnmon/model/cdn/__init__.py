import datetime
import functools
import ipaddress
import os
import tempfile
from dataclasses import dataclass
from dataclasses import field
from typing import List

import requests
import yaml

from cdnmon.util import bgpview
from cdnmon.util.cidr import deduplicate_networks


class ETL:
    def extract(self):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data):
        raise NotImplementedError


class CIDR(ETL):
    def ipv4_prefixes(self) -> List[str]:
        return self.transform(self.extract())["ipv4_prefixes"]

    def ipv6_prefixes(self) -> List[str]:
        return self.transform(self.extract())["ipv6_prefixes"]

    @functools.lru_cache(maxsize=None)
    def http_get(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36 "
        }
        return requests.get(url, headers=headers)


class BGPViewCIDR(CIDR):
    def __init__(self, query_term_list: List[str] = []):
        self.query_term_list = query_term_list
        self.bgpview_client = bgpview.BGPViewClient()

    def ipv4_prefixes(self) -> List[str]:
        ipv4_networks = []
        for query_term in self.query_term_list:
            data = self.bgpview_client.search(query_term)
            for item in data["data"]["ipv4_prefixes"]:
                ipv4_networks.append(str(ipaddress.IPv4Network(item["prefix"], strict=False)))
        return deduplicate_networks(ipv4_networks)

    def ipv6_prefixes(self) -> List[str]:
        ipv6_networks = []
        for query_term in self.query_term_list:
            data = self.bgpview_client.search(query_term)
            for item in data["data"]["ipv6_prefixes"]:
                ipv6_networks.append(str(ipaddress.IPv6Network(item["prefix"], strict=False)))
        return deduplicate_networks(ipv6_networks)


@dataclass
class CNAMEPattern:
    suffix: str = ""
    pattern: str = ""
    source: str = ""
    examples: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return self.suffix

    def __repr__(self) -> str:
        return self.suffix

    def marshal(self) -> dict:
        return {
            "suffix": self.suffix,
            "pattern": self.pattern,
            "source": self.source,
            "examples": self.examples,
        }


@dataclass
class CommonCDN:
    name: str
    asn_patterns: list[str] = field(default_factory=list)
    cname_suffixes: list[CNAMEPattern] = field(default_factory=list)

    def __init__(
        self,
        name: str,
        asn_patterns: List[str],
        cname_suffixes: List[CNAMEPattern],
        cidr: CIDR,
    ):
        self.name = name
        self.asn_patterns = asn_patterns
        self.cname_suffixes = cname_suffixes
        self.cidr = cidr

    def ipv4_prefixes(self) -> List[str]:
        return self.cidr.ipv4_prefixes()

    def ipv6_prefixes(self) -> List[str]:
        return self.cidr.ipv6_prefixes()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def dump(self) -> bool:
        path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__),
                    ),
                ),
            ),
            "assets",
            "cdn",
            f"{self.name}.yaml",
        )
        with open(path, mode="r", encoding="utf-8") as f:
            old_content = f.read()

        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            temporary_filename = f.name
            yaml.dump(
                {
                    "name": self.name,
                    "asn_patterns": self.asn_patterns,
                    "cname_suffixes": [i.marshal() for i in self.cname_suffixes],
                    "ipv4_prefixes": self.ipv4_prefixes(),
                    "ipv6_prefixes": self.ipv6_prefixes(),
                    "updated_at": datetime.datetime.now().isoformat(),
                },
                f,
            )

        with open(temporary_filename, mode="r", encoding="utf-8") as f:
            new_content = f.read()

        old_lines = [line for line in old_content.splitlines() if not line.startswith("updated_at:")]
        new_lines = [line for line in new_content.splitlines() if not line.startswith("updated_at:")]

        if old_lines != new_lines:
            # move temporary file to the original file
            os.replace(temporary_filename, path)
            return True
        else:
            # remove temporary file
            os.remove(temporary_filename)
            return False


__all__ = [
    "advancedhosting",
    "akamai",
    "alibaba_cdn",
    "alibaba_dcdn",
    "alibaba_waf",
    "asia_isp",
    "baidu",
    "baishan",
    "beluga",
    "bunny",
    "cachefly",
    "cdn77",
    "cdnetworks",
    "cdnvideo",
    "chinacache",
    "cloudflare",
    "cloudfront",
    "ctyun",
    "dnion",
    "douyin",
    "edgecast",
    "edgenext",
    "edgio",
    "fastly_edge_compute",
    "fastly",
    "frontdoor",
    "gcore",
    "google",
    "huawei",
    "imperva",
    "incapsula",
    "jingdong",
    "keycdn",
    "kingsoft",
    "leaseweb",
    "lumen",
    "maxcdn",
    "medianova",
    "qiniu",
    "tata_communications",
    "tencent",
    "ucloud",
    "upyun",
    "verizon",
    "volc",
    "wangsu",
]
