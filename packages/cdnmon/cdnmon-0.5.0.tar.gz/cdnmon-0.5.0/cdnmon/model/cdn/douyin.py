from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="douyin",
    asn_patterns=["bytedance", "douyin"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdnbuild.com"),
    ],
    cidr=BGPViewCIDR(["bytedance", "douyin"]),
)
