from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "akamai"
        self.ipv4_url = "https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip"
        self.ipv6_url = self.ipv4_url
        self.asn_patterns = ["akamai"]
        self.cname_suffixes = [
            ".edgesuite.net",
            ".edgekey.net",
            ".akamaized.net",
            ".akadns.net",
            ".akamai.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        """
        [1] https://techdocs.akamai.com/property-mgr/docs/origin-ip-access-control
        """
        import requests
        import zipfile
        import io

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36 "
        }
        content = requests.get(self.ipv4_url, headers=headers).content
        z = zipfile.ZipFile(io.BytesIO(content), mode="r")
        return {
            "ipv4": z.read("akamai_ipv4_CIDRs.txt").decode("utf-8"),
            "ipv6": z.read("akamai_ipv6_CIDRs.txt").decode("utf-8"),
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }
