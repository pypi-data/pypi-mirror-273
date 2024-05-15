from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="beluga",
    asn_patterns=["beluga"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["beluga"]),
)
