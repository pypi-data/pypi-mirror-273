from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="edgio",
    asn_patterns=["edgio"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["edgio"]),
)
