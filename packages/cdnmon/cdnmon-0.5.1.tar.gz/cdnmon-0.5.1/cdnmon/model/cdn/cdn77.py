from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdn77",
    asn_patterns=["cdn77"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["cdn77"]),
)
