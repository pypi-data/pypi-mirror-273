from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="baishan",
    asn_patterns=["baishan"],
    cname_suffixes=[
        CNAMEPattern(suffix=".bsgslb.cn", pattern=r"${domain}.bsgslb.cn"),
        CNAMEPattern(suffix=".trpcdn.net", pattern=r"${domain}.bsgslb.cn"),
    ],
    cidr=BGPViewCIDR(["baishan"]),
)
