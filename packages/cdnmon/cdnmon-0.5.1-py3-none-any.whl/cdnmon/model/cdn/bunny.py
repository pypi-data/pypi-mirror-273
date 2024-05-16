from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="bunny",
    asn_patterns=["bunny"],
    cname_suffixes=[
        CNAMEPattern(suffix=".b-cdn.net"),
    ],
    cidr=BGPViewCIDR(["bunny"]),
)
