from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="keycdn",
    asn_patterns=["keycdn"],
    cname_suffixes=[
        CNAMEPattern(suffix=".kxcdn.com"),
    ],
    cidr=BGPViewCIDR(["keycdn"]),
)
