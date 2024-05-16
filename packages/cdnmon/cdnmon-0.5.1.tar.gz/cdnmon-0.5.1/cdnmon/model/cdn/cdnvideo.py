from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdnvideo",
    asn_patterns=["cdnvideo"],
    cname_suffixes=[],
    cidr=BGPViewCIDR(["cdnvideo"]),
)
