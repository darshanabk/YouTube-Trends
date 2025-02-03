### JSON Format for Country Detail Requirement - Single Record (Country Data Sample)

```json
{
    "country_code": {                                 // ISO 3166-1 Alpha-2 code for the country (e.g., "IN")
        "country_name": "string",                     // Country Name (e.g., "India")
        "continent": "string",                        // Continent where the Country belongs to (e.g., "Asia")
        "continent_code": "string",                   // Continent Code where the Country belongs to (e.g., "AS")
        "it_hub_country": "string"                    // Whether the Country has an IT Hub ("Yes"/"No", e.g., "Yes")
    }
}
```
Below is a detailed tabular column for all the fields specified in the data structure. The column includes **Field Name**, **Min Length**, **Max Length**, **Value Type**, **Special Format/Notes**, and **KPI**. 

| **Field Name**                    | **Min Length** | **Max Length** | **Value Type**      | **Special Format/Notes**                                                                                    | **KPI** |
|-----------------------------------|----------------|----------------|---------------------|-------------------------------------------------------------------------------------------------------------|---------|
| `country_code`                    | 2              | 2              | String              | ISO 3166-1 Alpha-2 code for the country (e.g., `IN`)                                                        | No      |
| `country_name`                    | N/A            | N/A            | String              | Country Name (e.g., `India`)                                                                                | Yes     |
| `continent`                       | N/A            | N/A            | String              | Continent where the Country belongs to (e.g., `Asia`)                                                       | Yes     |
| `continent_code`                  | 2              | 2              | String              | Continent Code where the Country belongs to (e.g., `AS`)                                                    | Yes     |
| `it_hub_country`                  | 2              | 3              | String              | Whether the Country has an IT Hub ("Yes"/"No", e.g., `Yes`)                                                 | Yes     |
