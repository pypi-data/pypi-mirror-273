from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="imperva",
    asn_patterns=["imperva"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["imperva"]),
)
