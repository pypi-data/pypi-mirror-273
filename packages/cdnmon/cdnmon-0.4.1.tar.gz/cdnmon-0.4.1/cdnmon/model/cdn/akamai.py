from cdnmon.model.cdn import CIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.util.cidr import deduplicate_networks


class AkamaiCIDR(CIDR):
    ipv4_url: str = "https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip"
    ipv6_url: str = ipv4_url

    def extract(self):
        """
        [1] https://techdocs.akamai.com/property-mgr/docs/origin-ip-access-control
        """
        import zipfile
        import io

        content = self.http_get(AkamaiCIDR.ipv4_url).content
        z = zipfile.ZipFile(io.BytesIO(content), mode="r")
        return {
            "ipv4": z.read("akamai_ipv4_CIDRs.txt").decode("utf-8"),
            "ipv6": z.read("akamai_ipv6_CIDRs.txt").decode("utf-8"),
        }

    def transform(self, response: dict):
        ipv4_networks = [line.strip() for line in response["ipv4"].split("\n") if line.strip() != ""]
        ipv6_networks = [line.strip() for line in response["ipv6"].split("\n") if line.strip() != ""]
        return {
            "ipv4_prefixes": deduplicate_networks(ipv4_networks, filter_version=4),
            "ipv6_prefixes": deduplicate_networks(ipv6_networks, filter_version=6),
        }


CDN = CommonCDN(
    name="akamai",
    asn_patterns=["akamai"],
    cname_suffixes=[
        CNAMEPattern(suffix=".edgesuite.net", pattern=r"${domain}.edgesuite.net"),
        CNAMEPattern(suffix=".edgekey.net", pattern=r"${domain}.edgekey.net"),
        CNAMEPattern(suffix="-v1.akamaized.net", pattern=r"${domain}-v1.akamaized.net"),
        CNAMEPattern(suffix="-v1.edgekey.net", pattern=r"${domain}-v1.edgekey.net"),
        CNAMEPattern(suffix=".akadns.net"),
        CNAMEPattern(suffix=".akamai.net"),
    ],
    cidr=AkamaiCIDR(),
)
