from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="ctyun",
    asn_patterns=["ctyun", "chinanet"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ctadns.cn", pattern=r"${domain}.ctadns.cn"),
        CNAMEPattern(suffix=".ctacdn.cn", pattern=r"${domain}.ctacdn.cn"),
    ],
    cidr=BGPViewCIDR(["ctyun", "chinanet"]),
)
