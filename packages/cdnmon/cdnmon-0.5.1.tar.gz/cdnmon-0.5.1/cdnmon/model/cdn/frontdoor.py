from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="frontdoor",
    asn_patterns=["frontdoor", "azure", "microsoft"],
    cname_suffixes=[
        CNAMEPattern(suffix=".azurefd.net", pattern=r"${name}.azurefd.net"),
    ],
    cidr=BGPViewCIDR(["frontdoor", "azure", "microsoft"]),
)
