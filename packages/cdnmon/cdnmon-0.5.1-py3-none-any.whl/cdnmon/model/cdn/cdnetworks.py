from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdnetworks",
    asn_patterns=["cdnetworks"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["cdnetworks"]),
)
