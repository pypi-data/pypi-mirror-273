from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="chinacache",
    asn_patterns=["chinacache"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["chinacache"]),
)
