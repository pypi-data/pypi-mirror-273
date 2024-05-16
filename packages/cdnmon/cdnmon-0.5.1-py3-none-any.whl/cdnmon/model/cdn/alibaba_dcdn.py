from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="alibaba-dcdn",
    asn_patterns=["alibaba", "taobao", "alicloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".m.alikunlun.com", pattern=r"${domain}.m.alikunlun.com"),
        CNAMEPattern(suffix=".w.kunlunaq.com", pattern=r"${domain}.w.kunlunaq.com"),
        CNAMEPattern(suffix=".w.kunlunar.com", pattern=r"${domain}.w.kunlunar.com"),
        CNAMEPattern(suffix=".w.kunlunca.com", pattern=r"${domain}.w.kunlunca.com"),
        CNAMEPattern(suffix=".w.kunluncan.com", pattern=r"${domain}.w.kunluncan.com"),
        CNAMEPattern(suffix=".w.kunlunea.com", pattern=r"${domain}.w.kunlunea.com"),
        CNAMEPattern(suffix=".w.kunlungem.com", pattern=r"${domain}.w.kunlungem.com"),
        CNAMEPattern(suffix=".w.kunlungr.com", pattern=r"${domain}.w.kunlungr.com"),
        CNAMEPattern(suffix=".w.kunlunhuf.com", pattern=r"${domain}.w.kunlunhuf.com"),
        CNAMEPattern(suffix=".w.kunlunle.com", pattern=r"${domain}.w.kunlunle.com"),
        CNAMEPattern(suffix=".w.kunlunno.com", pattern=r"${domain}.w.kunlunno.com"),
        CNAMEPattern(suffix=".w.kunlunpi.com", pattern=r"${domain}.w.kunlunpi.com"),
        CNAMEPattern(suffix=".w.kunlunsl.com", pattern=r"${domain}.w.kunlunsl.com"),
        CNAMEPattern(suffix=".w.kunlunso.com", pattern=r"${domain}.w.kunlunso.com"),
    ],
    cidr=BGPViewCIDR(["alibaba", "taobao", "alicloud"]),
)
