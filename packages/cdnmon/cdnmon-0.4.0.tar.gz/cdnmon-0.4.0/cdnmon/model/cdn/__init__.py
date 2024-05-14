from abc import ABC, abstractmethod
from cdnmon.util import bgpview
import os
import yaml
import datetime


class AbstractCDN(ABC):
    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, response):
        pass

    def dump(self):
        self.transform(self.extract())
        path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__),
                    ),
                ),
            ),
            "assets",
            "cdn",
            f"{self.abbreviation}.yaml",
        )
        with open(path, "w") as f:
            yaml.dump(
                {
                    "name": self.abbreviation,
                    "asn_patterns": self.asn_patterns,
                    "cname_suffixes": self.cname_suffixes,
                    "ipv4_prefixes": self.ipv4_prefixes,
                    "ipv6_prefixes": self.ipv6_prefixes,
                    "updated_at": datetime.datetime.now().isoformat(),
                },
                f,
            )


class AbstractBGPViewCDN(AbstractCDN):
    def __init__(self, abbreviation, query_term=None):
        self.abbreviation = abbreviation
        self.query_term = query_term or self.abbreviation
        self.bgpview_client = bgpview.BGPViewClient()

    def extract(self):
        return self.bgpview_client.extract(self.query_term)

    def transform(self, data):
        return self.bgpview_client.transform(data)
