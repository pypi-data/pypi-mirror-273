from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="jingdong",
    asn_patterns=["jingdong"],
    cname_suffixes=[
        CNAMEPattern(suffix=".dy.galileo.jcloud-cdn.com", pattern=r"${domain}.dy.galileo.jcloud-cdn.com"),
        CNAMEPattern(suffix=".cdn.jcloudcdn.com", pattern=r"${domain}.cdn.jcloudcdn.com"),
        CNAMEPattern(suffix=".jcloudcache.com", pattern=r"${domain}.lk-[0-9a-f]{6}.jcloudcache.com"),
        CNAMEPattern(suffix=".cdn.jcloudcache.com", pattern=r"${domain}.lk-[0-9a-f]{6}.cdn.jcloudcache.com"),
        CNAMEPattern(suffix=".jcloudimg.com"),
        CNAMEPattern(suffix=".gslb.qianxun.com", pattern=r"${domain}.gslb.qianxun.com"),
    ],
    cidr=BGPViewCIDR(["jingdong"]),
)
