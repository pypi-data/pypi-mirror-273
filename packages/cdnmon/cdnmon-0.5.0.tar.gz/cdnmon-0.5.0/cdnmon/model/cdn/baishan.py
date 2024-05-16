from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="baishan",
    asn_patterns=["baishan"],
    cname_suffixes=[
        CNAMEPattern(suffix=".bsgslb.cn"),
        CNAMEPattern(suffix=".trpcdn.net"),
    ],
    cidr=BGPViewCIDR(["baishan"]),
)
