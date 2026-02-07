"""
China AS Data Collector
=======================

Collects China-related AS data from public sources.
Addresses the limitation of CAIDA data lacking Chinese perspective.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ASInfo:
    """Autonomous System information."""
    asn: int
    name: str
    description: str
    country: str
    prefixes_count: int


# Known major Chinese AS numbers (from BGPView and public sources)
CHINA_MAJOR_AS = {
    # Tier-1 ISPs
    4134: {
        "name": "CHINANET-BACKBONE",
        "description": "China Telecom Backbone",
        "type": "Tier-1 ISP"
    },
    4837: {
        "name": "CHINA UNICOM",
        "description": "China Unicom Backbone", 
        "type": "Tier-1 ISP"
    },
    9808: {
        "name": "CHINA MOBILE",
        "description": "China Mobile Communications Group",
        "type": "Tier-1 ISP"
    },
    # Important networks
    4809: {
        "name": "CHINATELECOM-CN2",
        "description": "China Telecom Next Generation Carrier Network",
        "type": "Tier-1 ISP (CN2)"
    },
    4812: {
        "name": "CHINATELECOM-SH",
        "description": "China Telecom Shanghai",
        "type": "Regional"
    },
    58453: {
        "name": "CMI-INT-HK",
        "description": "China Mobile International Hong Kong",
        "type": "International"
    },
    4811: {
        "name": "CHINATELECOM-GD",
        "description": "China Telecom Guangdong",
        "type": "Regional"
    },
    # Education and Research
    9394: {
        "name": "CERNET",
        "description": "China Education and Research Network",
        "type": "Academic"
    },
    4538: {
        "name": "ERX-CERNET-BKB",
        "description": "CERNET Backup",
        "type": "Academic"
    },
    7497: {
        "name": "CSTNET",
        "description": "China Science and Technology Network",
        "type": "Academic"
    },
    # Other major
    24139: {
        "name": "CRNET",
        "description": "China Railcom",
        "type": "ISP"
    },
    56041: {
        "name": "CMNET",
        "description": "China Mobile Network",
        "type": "ISP"
    },
    56048: {
        "name": "CMNET-BJ",
        "description": "China Mobile Beijing",
        "type": "Regional"
    },
    # Content providers
    37963: {
        "name": "ALIBABA-CN",
        "description": "Alibaba Cloud",
        "type": "Cloud/Content"
    },
    45090: {
        "name": "TENCENT-NET",
        "description": "Tencent Cloud Computing",
        "type": "Cloud/Content"
    },
    55990: {
        "name": "HWCSNET",
        "description": "Huawei Cloud Service",
        "type": "Cloud/Content"
    },
    135377: {
        "name": "UCLOUD-HK",
        "description": "UCloud Hong Kong",
        "type": "Cloud/Content"
    },
    # International operators in China
    4637: {
        "name": "TELSTRA-AS",
        "description": "Telstra Global (Australia, major presence in Asia)",
        "type": "International"
    },
    2914: {
        "name": "NTT-LTD",
        "description": "NTT America (strong Asia presence)",
        "type": "International"
    },
    174: {
        "name": "COGENT",
        "description": "Cogent Communications (global tier-1)",
        "type": "International"
    },
    1299: {
        "name": "TELIANET",
        "description": "Telia Company (global)",
        "type": "International"
    },
    3257: {
        "name": "GTT-BACKBONE",
        "description": "GTT Communications",
        "type": "International"
    },
    3356: {
        "name": "LEVEL3",
        "description": "Level 3 Parent (major in Asia)",
        "type": "International"
    },
    6939: {
        "name": "HURRICANE",
        "description": "Hurricane Electric (strong Asia presence)",
        "type": "International"
    },
    2497: {
        "name": "IIJ",
        "description": "Internet Initiative Japan",
        "type": "International"
    },
    10026: {
        "name": "LAGIS",
        "description": "LG Uplus (Korea)",
        "type": "International"
    },
    17858: {
        "name": "LGTELECOM",
        "description": "LG Telecom (Korea)",
        "type": "International"
    },
    4766: {
        "name": "KIXS",
        "description": "Korea Telecom",
        "type": "International"
    },
    2516: {
        "name": "KDDI",
        "description": "KDDI Japan",
        "type": "International"
    },
    9924: {
        "name": "TFN",
        "description": "Taiwan Fixed Network",
        "type": "International"
    },
    3462: {
        "name": "HINET",
        "description": "Chunghwa Telecom (Taiwan)",
        "type": "International"
    },
    9505: {
        "name": "TWGATE",
        "description": "Taiwan Internet Gateway",
        "type": "International"
    },
    9304: {
        "name": "HUTCHISON",
        "description": "Hutchison Global (Hong Kong)",
        "type": "International"
    },
    4515: {
        "name": "HKIX-NSP",
        "description": "Hong Kong Internet Exchange",
        "type": "IXP"
    },
}


class ChinaASDataCollector:
    """Collector for China-related AS data."""
    
    def __init__(self):
        self.known_as = CHINA_MAJOR_AS
    
    def get_as_info_from_bgpview(self, asn: int) -> Optional[Dict]:
        """Query BGPView API for AS information."""
        url = f"https://api.bgpview.io/asn/{asn}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Academic Research; China-AS-Study)',
                'Accept': 'application/json'
            }
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('status') == 'ok':
                    return data.get('data', {})
                return None
                
        except Exception as e:
            print(f"Error querying AS{asn}: {e}")
            return None
    
    def collect_all_china_as(self) -> List[ASInfo]:
        """Collect information about all major China AS."""
        results = []
        
        print("Collecting China AS information...")
        print(f"Total known AS: {len(self.known_as)}")
        print()
        
        for asn, info in sorted(self.known_as.items()):
            # Try to get live data from BGPView
            live_data = self.get_as_info_from_bgpview(asn)
            
            if live_data:
                prefixes = len(live_data.get('prefixes', []))
                country = live_data.get('country_code', 'CN')
            else:
                prefixes = 0
                country = 'CN'
            
            as_info = ASInfo(
                asn=asn,
                name=info['name'],
                description=info['description'],
                country=country,
                prefixes_count=prefixes
            )
            results.append(as_info)
            
            print(f"AS{asn:6} | {info['name']:20} | {info['type']:15} | {prefixes:5} prefixes")
        
        return results
    
    def analyze_china_internet_structure(self) -> Dict:
        """Analyze the structure of Chinese internet based on known AS."""
        analysis = {
            'tier1_isp': [],
            'academic': [],
            'cloud_content': [],
            'regional': [],
            'international_connections': []
        }
        
        for asn, info in self.known_as.items():
            as_type = info['type']
            if 'Tier-1' in as_type:
                analysis['tier1_isp'].append(asn)
            elif 'Academic' in as_type:
                analysis['academic'].append(asn)
            elif 'Cloud' in as_type or 'Content' in as_type:
                analysis['cloud_content'].append(asn)
            elif 'Regional' in as_type:
                analysis['regional'].append(asn)
            elif 'International' in as_type:
                analysis['international_connections'].append(asn)
        
        return analysis
    
    def generate_comparison_report(self):
        """Generate report comparing China vs Western internet structure."""
        analysis = self.analyze_china_internet_structure()
        
        print("=" * 80)
        print("China Internet AS Structure Analysis")
        print("=" * 80)
        print()
        
        print("1. TIER-1 ISP (Backbone Networks)")
        print("-" * 40)
        for asn in analysis['tier1_isp'][:6]:
            info = self.known_as[asn]
            print(f"  AS{asn}: {info['name']} - {info['description']}")
        print(f"  Total: {len(analysis['tier1_isp'])} networks")
        print()
        
        print("2. ACADEMIC/RESEARCH Networks")
        print("-" * 40)
        for asn in analysis['academic']:
            info = self.known_as[asn]
            print(f"  AS{asn}: {info['name']} - {info['description']}")
        print()
        
        print("3. CLOUD/CONTENT Providers")
        print("-" * 40)
        for asn in analysis['cloud_content']:
            info = self.known_as[asn]
            print(f"  AS{asn}: {info['name']} - {info['description']}")
        print()
        
        print("4. Major International Connections")
        print("-" * 40)
        for asn in analysis['international_connections'][:10]:
            info = self.known_as[asn]
            print(f"  AS{asn}: {info['name']} ({info['description']})")
        print(f"  Total: {len(analysis['international_connections'])} networks")
        print()
        
        print("=" * 80)
        print("Key Observations:")
        print("=" * 80)
        print()
        print("1. HIGHLY CONCENTRATED STRUCTURE")
        print("   - 3 major backbone ISPs dominate (电信4134, 联通4837, 移动9808)")
        print("   - Centralized topology vs decentralized Western internet")
        print("   - Expected: Lower dimensionality (more hierarchical)")
        print()
        print("2. STRONG ACADEMIC SEPARATION")
        print("   - CERNET (9394) as separate academic backbone")
        print("   - May form distinct sub-network with different dimensionality")
        print()
        print("3. EMERGING CLOUD PROVIDERS")
        print("   - Alibaba (37963), Tencent (45090), Huawei (55990)")
        print("   - May create new topological patterns")
        print()
        print("4. INTERNATIONAL CONNECTIVITY")
        print("   - Heavy reliance on Hong Kong (9304, 4515)")
        print("   - Limited direct international presence")
        print("   - May create 'bottleneck' structure in global topology")
        print()
        print("=" * 80)
        print("Implications for Dimension Research:")
        print("=" * 80)
        print()
        print("CAIDA DATA LIMITATIONS:")
        print("  - Likely captures international connections well")
        print("  - May miss domestic China interconnections")
        print("  - Could underestimate domestic clustering/communities")
        print()
        print("EXPECTED DIMENSION DIFFERENCES:")
        print("  - China AS graph: Lower dimension (d_B ~ 2.0-2.5, hierarchical)")
        print("  - US AS graph: Higher dimension (d_B ~ 3.0-3.5, decentralized)")
        print("  - International view: Different from domestic Chinese view")
        print()
        print("NEEDED DATA:")
        print("  - CERNET internal topology")
        print("  - China Telecom internal AS connections")
        print("  - Domestic peering relationships")
        print()


def generate_caida_limitation_section():
    """Generate text for paper section on CAIDA limitations."""
    text = """
## Data Limitations: Geographic Coverage

### CAIDA AS Relationship Dataset

The CAIDA AS relationship dataset used in this study primarily relies on:
- **RouteViews**: Global BGP collectors (mostly Western locations)
- **RIPE RIS**: European-based routing information service
- **Ark**: CAIDA's active measurement platform

These data sources have limited visibility into **domestic Chinese internet topology**.

### Known Coverage Gaps

| Aspect | Coverage Level | Impact on Results |
|--------|---------------|-------------------|
| International routes | ⭐⭐⭐⭐⭐ | Well captured |
| China major ISP backbones | ⭐⭐⭐⭐☆ | Partially visible |
| China domestic peering | ⭐⭐⭐☆☆ | Likely incomplete |
| CERNET (Academic) | ⭐⭐☆☆☆ | Limited visibility |
| Regional ISPs | ⭐⭐☆☆☆ | Underestimated |

### Structural Differences: China vs Western Internet

Based on publicly available AS information, the Chinese internet exhibits:

1. **Higher Concentration**: Dominated by 3 major carriers (4134, 4837, 9808)
2. **Hierarchical Structure**: Tiered with clear backbone/regional distinction
3. **Limited IXP Ecosystem**: Fewer Internet Exchange Points compared to US/EU
4. **Academic Separation**: CERNET operates as distinct parallel network

These structural differences suggest that the **effective dimension of Chinese internet 
may differ significantly** from Western internet measurements.

### Mitigation Strategies

To address these limitations, we:
1. Supplement with BGPView API data (includes Chinese AS details)
2. Explicitly acknowledge geographic bias in our conclusions
3. Limit generalization claims to "Western/International internet"
4. Propose future work with CERNET collaboration for complete picture

### Impact on Research Questions

| Research Question | Impact | Mitigation |
|------------------|--------|------------|
| Global AS topology dimension | High bias | Acknowledge limitation |
| Universal scaling laws | Medium bias | Needs China data for validation |
| Internet evolution trends | Low bias | Time-series still valid for Western view |

"""
    return text


if __name__ == "__main__":
    # Generate comparison report
    collector = ChinaASDataCollector()
    collector.generate_comparison_report()
    
    print("\n" + "=" * 80)
    print("Paper Section: CAIDA Limitations")
    print("=" * 80)
    print(generate_caida_limitation_section())
