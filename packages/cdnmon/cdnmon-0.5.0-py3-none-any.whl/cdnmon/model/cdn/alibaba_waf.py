from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="alibaba-waf",
    asn_patterns=["alibaba", "taobao", "alicloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".yundunwaf1.com"),
        CNAMEPattern(suffix=".yundunwaf2.com"),
        CNAMEPattern(suffix=".yundunwaf3.com"),
        CNAMEPattern(suffix=".yundunwaf4.com"),
        CNAMEPattern(suffix=".yundunwaf5.com"),
    ],
    cidr=BGPViewCIDR(["alibaba", "taobao", "alicloud"]),
)
