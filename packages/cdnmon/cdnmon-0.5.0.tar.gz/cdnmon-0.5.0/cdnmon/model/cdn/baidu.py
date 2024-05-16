from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="baidu",
    asn_patterns=["baidu"],
    cname_suffixes=[
        CNAMEPattern(suffix=".a.bdydns.com"),
        CNAMEPattern(suffix=".yjs-cdn.com"),
        CNAMEPattern(suffix=".yunjiasu-cdn.net"),
    ],
    cidr=BGPViewCIDR(["baidu"]),
)
