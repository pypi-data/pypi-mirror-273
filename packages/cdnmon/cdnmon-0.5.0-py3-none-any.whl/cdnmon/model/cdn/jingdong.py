from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="jingdong",
    asn_patterns=["jingdong"],
    cname_suffixes=[
        CNAMEPattern(suffix=".dy.galileo.jcloud-cdn.com"),
        CNAMEPattern(suffix=".cdn.jcloudcdn.com"),
        CNAMEPattern(suffix=".jcloudcache.com"),
        CNAMEPattern(suffix=".cdn.jcloudcache.com"),
    ],
    cidr=BGPViewCIDR(["jingdong"]),
)
