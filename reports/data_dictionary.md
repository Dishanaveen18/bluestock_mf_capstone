# Data Dictionary Blueprint - Mutual Fund Database Layout

### 1. `dim_fund` (Lookup Dimensions Table)
| Field Name | Storage Data Type | Core Constraints | Logical System Definitions |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Unique Association Code assigned by AMFI |
| `fund_house` | TEXT | NOT NULL | Asset Management Company holding entity title |
| `scheme_name` | TEXT | NOT NULL | Complete designated investment name label |
| `category` | TEXT | - | Asset Allocation Division Category |
| `aum_crore` | REAL | - | Assets Under Management volume in Indian Crore Units |

### 2. `fact_nav` (Historical Metric Fact Table)
| Field Name | Storage Data Type | Core Constraints | Logical System Definitions |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique record ID tracker |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund` identity mapping |
| `nav_date` | TEXT (YYYY-MM-DD) | NOT NULL | Valuation marker date timestamp tracking |
| `nav` | REAL | NOT NULL | Close pricing valuation metric calculation anchor |
| `daily_return` | REAL | - | Single trading session relative return margin yield |