from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cachefly",
    asn_patterns=["cachefly"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["cachefly"]),
)
