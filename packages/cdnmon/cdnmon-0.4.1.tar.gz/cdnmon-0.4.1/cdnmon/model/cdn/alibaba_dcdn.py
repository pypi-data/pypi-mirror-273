from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="alibaba-dcdn",
    asn_patterns=["alibaba", "taobao", "alicloud"],
    cname_suffixes=[
        CNAMEPattern(suffix=".m.alikunlun.com"),
        CNAMEPattern(suffix=".w.kunlunaq.com"),
        CNAMEPattern(suffix=".w.kunlunar.com"),
        CNAMEPattern(suffix=".w.kunlunca.com"),
        CNAMEPattern(suffix=".w.kunluncan.com"),
        CNAMEPattern(suffix=".w.kunlunea.com"),
        CNAMEPattern(suffix=".w.kunlungem.com"),
        CNAMEPattern(suffix=".w.kunlungr.com"),
        CNAMEPattern(suffix=".w.kunlunhuf.com"),
        CNAMEPattern(suffix=".w.kunlunle.com"),
        CNAMEPattern(suffix=".w.kunlunno.com"),
        CNAMEPattern(suffix=".w.kunlunpi.com"),
        CNAMEPattern(suffix=".w.kunlunsl.com"),
        CNAMEPattern(suffix=".w.kunlunso.com"),
    ],
    cidr=BGPViewCIDR(["alibaba", "taobao", "alicloud"]),
)
