from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="dnion",
    asn_patterns=["dnion"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["dnion"]),
)
