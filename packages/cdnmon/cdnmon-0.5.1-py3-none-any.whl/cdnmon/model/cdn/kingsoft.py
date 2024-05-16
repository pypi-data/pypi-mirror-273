from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="kingsoft",
    asn_patterns=["kingsoft", "ksyun"],
    cname_suffixes=[
        CNAMEPattern(suffix=".download.ks-cdn.com", pattern=r"${domain}.download.ks-cdn.com"),
        CNAMEPattern(suffix=".ksyuncdn.com"),
    ],
    cidr=BGPViewCIDR(["kingsoft", "ksyun"]),
)
