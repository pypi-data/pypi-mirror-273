from cdnmon.model.cdn import AbstractCDN
from cdnmon.util.cidr import deduplicate_networks
from cdnmon.util.aws import get_ip_range_of_aws


class CDN(AbstractCDN):
    def __init__(self):
        self.abbreviation = "cloudfront"
        self.ipv4_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
        self.ipv6_url = self.ipv4_url
        self.asn_patterns = [
            "cloudfront",
            "amazon",
        ]
        self.cname_suffixes = [
            ".cloudfront.net",
        ]
        self.ipv4_prefixes = self.transform(self.extract())["ipv4_prefixes"]
        self.ipv6_prefixes = self.transform(self.extract())["ipv6_prefixes"]

    def extract(self):
        """
        [1] https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
        """
        ipv4_networks, ipv6_networks = get_ip_range_of_aws("CLOUDFRONT")
        return {
            "ipv4": "\n".join(ipv4_networks),
            "ipv6": "\n".join(ipv6_networks),
        }

    def transform(self, response):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }
