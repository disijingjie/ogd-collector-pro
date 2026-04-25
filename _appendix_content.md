## Appendix G Data Collection Log Samples

### G.1 Collection Task Execution Log

The following is an excerpt from OGD-Collector Pro's complete collection log for Zhejiang Data Open Platform, demonstrating the full workflow from task initiation to data storage.

```
[2025-03-15 09:23:14] INFO: Task started - Platform: Zhejiang, URL: https://data.zjzwfw.gov.cn
[2025-03-15 09:23:15] INFO: Precheck passed - Response time: 0.89s, Structure match: 98.7%
[2025-03-15 09:23:16] INFO: List page collection started - Page: 1
[2025-03-15 09:23:18] INFO: List page success - Datasets this page: 20, Total: 20
...
[2025-03-15 09:35:47] INFO: List collection completed - Total pages: 785, Total datasets: 15,700
[2025-03-15 09:35:48] INFO: Detail page collection started - Batch: 1/157
[2025-03-15 09:35:52] INFO: Detail page success - ID: ZJ-00001, Title: "Zhejiang 2024 Statistical Yearbook"
[2025-03-15 09:35:55] WARN: Missing fields - ID: ZJ-00023, Missing: data_dictionary
[2025-03-15 11:42:33] INFO: Detail collection completed - Success: 15,632, Failed: 68, Rate: 99.57%
[2025-03-15 11:42:35] INFO: Parsing started - Parser: BeautifulSoup+XPath
[2025-03-15 11:42:48] INFO: Parsing completed - Parsed: 15,632, Anomalies: 127
[2025-03-15 11:42:50] INFO: Quality validation started
[2025-03-15 11:43:12] INFO: Validation completed - Passed: 15,505, Review needed: 127
[2025-03-15 11:43:15] INFO: Storage completed - SQLite: 15,632 records
[2025-03-15 11:43:17] INFO: Task completed - Duration: 2h19m53s
```

### G.2 Exception Handling Records

**Table G-1 Collection Exception Types and Handling Summary**

| Exception Type | Platforms Affected | Manifestation | Handling Measure | Result |
|:---|:---:|:---|:---|:---|
| Page structure change | 3 | CSS selector failure | Fallback to regex parser | Success |
| Anti-bot triggered | 5 | 403/503 errors | Reduce frequency, proxy pool | 4 success, 1 manual |
| Dynamic load timeout | 2 | JS render timeout | Increase wait to 10s | Success |
| Encoding inconsistency | 4 | Declared UTF-8 but GBK | Auto-detect and convert | Success |
| Data format anomaly | 6 | JSON parse failure | Fault-tolerant parser | Partial success |
| SSL certificate error | 1 | Expired certificate | Skip verification | Success |

### G.3 Manual Verification Records

**Table G-2 Manual Verification Workload and Consistency**

| Indicator | Platforms | Sample Size | Rater A | Rater B | Rater C | Kappa |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Data accuracy | 22 | 220 datasets | 98.2% | 97.8% | 98.5% | 0.89 |
| Metadata completeness | 28 | 280 datasets | 96.5% | 97.1% | 95.9% | 0.85 |
| API doc quality | 12 | 36 APIs | 94.3% | 95.1% | 93.8% | 0.82 |
| UX evaluation | 28 | 28 platforms | 92.1% | 93.4% | 91.8% | 0.79 |
| Policy completeness | 28 | 56 documents | 99.1% | 98.7% | 99.3% | 0.94 |


## Appendix H DEMATEL Expert Rating Raw Data

### H.1 Expert Background

**Table H-1 DEMATEL Expert Background Information**

| ID | Title | Field | Years | Platforms Known |
|:---:|:---|:---|:---:|:---:|
| E1 | Professor | Digital governance | 18 | 25+ |
| E2 | Associate Prof. | Info resource mgmt | 15 | 20+ |
| E3 | Researcher | Public policy | 12 | 18+ |
| E4 | Senior Engineer | Platform architecture | 10 | 15+ |
| E5 | Operations Director | Data platform ops | 8 | 12+ |
| E6 | Product Manager | Data products | 7 | 10+ |
| E7 | Deputy Director | Data open policy | 14 | 22+ |
| E8 | Section Chief | E-government | 11 | 16+ |

### H.2 Expert Rating Consistency

Kendall's W coefficient for 8 experts: W=0.74 (p<0.001), indicating high consistency. All individual Spearman correlations with group mean: 0.68-0.82 (p<0.001).


## Appendix I Platform Performance Raw Data

### I.1 TOPSIS Raw Scores

**Table I-1 TOPSIS Performance Evaluation Raw Scores (22 Platforms)**

| Rank | Province | Supply | Service | Quality | Effect | Equity | Overall |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Zhejiang | 0.92 | 0.88 | 0.91 | 0.85 | 0.78 | 0.87 |
| 2 | Guangdong | 0.89 | 0.85 | 0.87 | 0.82 | 0.75 | 0.84 |
| 3 | Shanghai | 0.85 | 0.87 | 0.86 | 0.79 | 0.80 | 0.83 |
| 4 | Beijing | 0.82 | 0.84 | 0.88 | 0.76 | 0.82 | 0.81 |
| 5 | Shandong | 0.88 | 0.79 | 0.82 | 0.71 | 0.68 | 0.78 |
| 6 | Guizhou | 0.75 | 0.72 | 0.78 | 0.68 | 0.65 | 0.72 |
| 7 | Fujian | 0.70 | 0.74 | 0.76 | 0.62 | 0.60 | 0.68 |
| 8 | Sichuan | 0.68 | 0.70 | 0.73 | 0.58 | 0.62 | 0.66 |
| 9 | Hubei | 0.65 | 0.68 | 0.71 | 0.55 | 0.58 | 0.63 |
| 10 | Jiangsu | 0.72 | 0.75 | 0.69 | 0.52 | 0.55 | 0.65 |
| 11 | Chongqing | 0.62 | 0.65 | 0.68 | 0.56 | 0.54 | 0.61 |
| 12 | Hainan | 0.58 | 0.60 | 0.65 | 0.50 | 0.52 | 0.58 |
| 13 | Hunan | 0.55 | 0.58 | 0.62 | 0.48 | 0.50 | 0.55 |
| 14 | Anhui | 0.52 | 0.55 | 0.60 | 0.45 | 0.48 | 0.53 |
| 15 | Jiangxi | 0.50 | 0.52 | 0.58 | 0.42 | 0.46 | 0.50 |
| 16 | Tianjin | 0.48 | 0.50 | 0.55 | 0.40 | 0.44 | 0.48 |
| 17 | Liaoning | 0.45 | 0.48 | 0.52 | 0.38 | 0.42 | 0.46 |
| 18 | Jilin | 0.42 | 0.45 | 0.50 | 0.35 | 0.40 | 0.43 |
| 19 | Inner Mongolia | 0.40 | 0.42 | 0.48 | 0.33 | 0.38 | 0.41 |
| 20 | Heilongjiang | 0.38 | 0.40 | 0.45 | 0.30 | 0.35 | 0.38 |
| 21 | Guangxi | 0.35 | 0.38 | 0.42 | 0.32 | 0.36 | 0.37 |
| 22 | Xinjiang | 0.32 | 0.35 | 0.40 | 0.28 | 0.33 | 0.34 |

*Note: All dimension scores are 0-1 standardized. Overall score uses AHP-entropy combined weighting.*

### I.2 DEA Efficiency Raw Data

**Table I-2 DEA-BCC Efficiency Evaluation Results**

| Province | Input1(Years) | Input2(Datasets) | Input3(Budget) | Output1(TOPSIS) | Output2(Apps) | Output3(API) | Theta | RTS |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Zhejiang | 10 | 15700 | 8500 | 0.87 | 245 | 125000 | 1.000 | CRS |
| Guangdong | 9 | 12800 | 7800 | 0.84 | 198 | 98000 | 1.000 | CRS |
| Shanghai | 8 | 9500 | 7200 | 0.83 | 156 | 87000 | 1.000 | CRS |
| Beijing | 9 | 8200 | 6900 | 0.81 | 142 | 76000 | 1.000 | CRS |
| Shandong | 8 | 60000 | 5500 | 0.78 | 89 | 45000 | 0.925 | IRS |
| Guizhou | 10 | 28000 | 4200 | 0.72 | 67 | 32000 | 0.856 | IRS |
| Fujian | 7 | 5600 | 3800 | 0.68 | 45 | 21000 | 0.789 | IRS |
| Sichuan | 7 | 4900 | 3600 | 0.66 | 38 | 18000 | 0.745 | IRS |
| Hubei | 7 | 3800 | 3400 | 0.63 | 32 | 15000 | 0.698 | IRS |
| Jiangsu | 8 | 7800 | 5800 | 0.65 | 41 | 19000 | 0.712 | IRS |

*Note: Budget is estimated (10k CNY/year). RTS: Returns to Scale (CRS=constant, IRS=increasing)*


## Appendix J Core Code Snippets

### J.1 Collector Base Class

```python
# collector/base.py
from abc import ABC, abstractmethod
from typing import List, Dict
import logging

class BaseCollector(ABC):
    def __init__(self, platform_config: Dict):
        self.config = platform_config
        self.platform_name = platform_config.get('name')
        self.base_url = platform_config.get('base_url')
        self.logger = logging.getLogger(f"collector.{self.platform_name}")
        
    @abstractmethod
    def login(self) -> bool:
        pass
    
    @abstractmethod  
    def get_dataset_list(self, page: int = 1) -> List[Dict]:
        pass
    
    @abstractmethod
    def get_dataset_detail(self, dataset_id: str) -> Dict:
        pass
    
    def collect_all(self) -> Dict:
        results = {'platform': self.platform_name, 'datasets': [], 'errors': []}
        try:
            if not self.precheck():
                raise ConnectionError(f"Precheck failed: {self.platform_name}")
            page = 1
            while True:
                datasets = self.get_dataset_list(page)
                if not datasets:
                    break
                results['datasets'].extend(datasets)
                page += 1
            for ds in results['datasets']:
                try:
                    detail = self.get_dataset_detail(ds['id'])
                    ds.update(detail)
                except Exception as e:
                    results['errors'].append({'id': ds['id'], 'error': str(e)})
        except Exception as e:
            self.logger.error(f"Collection failed: {e}")
            results['fatal_error'] = str(e)
        return results
    
    def precheck(self) -> bool:
        try:
            resp = self.session.get(self.base_url, timeout=10)
            return resp.status_code == 200
        except:
            return False
```

### J.2 Data Quality Validator

```python
# collector/validator.py
import re
from datetime import datetime
from typing import Dict, List, Tuple

class DataValidator:
    RULES = {
        'title': {'required': True, 'min_len': 5, 'max_len': 200},
        'publisher': {'required': True, 'pattern': r'^[\u4e00-\u9fa5]+'},
        'update_date': {'required': True, 'format': '%Y-%m-%d'},
        'format': {'required': True, 'options': ['CSV','JSON','XML','XLSX']},
        'download_url': {'required': True, 'pattern': r'^https?://'}
    }
    
    def validate(self, dataset: Dict) -> Tuple[bool, List[str]]:
        errors = []
        for field, rules in self.RULES.items():
            value = dataset.get(field)
            if rules.get('required') and not value:
                errors.append(f"{field}: required field missing")
                continue
            if not value:
                continue
            if 'min_len' in rules and len(str(value)) < rules['min_len']:
                errors.append(f"{field}: too short")
            if 'format' in rules and field == 'update_date':
                try:
                    datetime.strptime(str(value), rules['format'])
                except:
                    errors.append(f"{field}: invalid date format")
            if 'pattern' in rules:
                if not re.match(rules['pattern'], str(value)):
                    errors.append(f"{field}: format mismatch")
            if 'options' in rules:
                if str(value).upper() not in rules['options']:
                    errors.append(f"{field}: non-standard format")
        return len(errors) == 0, errors
```
