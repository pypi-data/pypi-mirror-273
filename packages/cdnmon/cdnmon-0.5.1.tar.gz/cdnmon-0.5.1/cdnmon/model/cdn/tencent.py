from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="tencent",
    asn_patterns=["tencent"],
    cname_suffixes=[
        CNAMEPattern(suffix=".dsa.dnsv1.com", pattern=r"${domain}.dsa.dnsv1.com"),
        CNAMEPattern(suffix=".dsa.dnsv1.com.cn", pattern=r"${domain}.dsa.dnsv1.com.cn"),
        CNAMEPattern(suffix=".cdn.dnsv1.com", pattern=r"${domain}.cdn.dnsv1.com"),
        CNAMEPattern(suffix=".cdn.dnsv1.com.cn", pattern=r"${domain}.cdn.dnsv1.com.cn"),
        CNAMEPattern(suffix=".eo.dnse0.com", pattern=r"${domain}.eo.dnse0.com"),
        CNAMEPattern(suffix=".eo.dnse1.com", pattern=r"${domain}.eo.dnse1.com"),
        CNAMEPattern(suffix=".eo.dnse2.com", pattern=r"${domain}.eo.dnse2.com"),
        CNAMEPattern(suffix=".eo.dnse3.com", pattern=r"${domain}.eo.dnse3.com"),
        CNAMEPattern(suffix=".eo.dnse4.com", pattern=r"${domain}.eo.dnse4.com"),
        CNAMEPattern(suffix=".eo.dnse5.com", pattern=r"${domain}.eo.dnse5.com"),
        CNAMEPattern(suffix=".cdn.qcloudcdn.cn", pattern=r"${domain}.cdn.qcloudcdn.cn"),
        CNAMEPattern(suffix=".txlivecdn.com", pattern=r"${domain}.txlivecdn.com"),
        CNAMEPattern(suffix=".ovscdns.com", pattern=r"${domain}.ovscdns.com"),
    ],
    cidr=BGPViewCIDR(query_term_list=["tencent"]),
)
