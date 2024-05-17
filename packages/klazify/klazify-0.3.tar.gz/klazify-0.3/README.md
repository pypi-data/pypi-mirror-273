# [![Klazify](https://www.klazify.com/img/new_klazify_logo.png)](https://klazify.com)

**Klazify** - The most accurate Content Classification API.
All-in-one domain data source. Get Website Logos, Company Data, Categorization and much more from a URL or Email.

## Key Features:

- AI Powered Real-Time Categorization.
- IAB Categorization.
- Full Path URL support
- Batch Enrichement importing a .CSV.
- Extract Logo from any URL
- Social Media Links Scraper API.
- Multi-site license. 
- Service-level agreement (SLA).

## Documentation

For comprehensive details regarding API endpoints, usage, and integration guidelines, please refer to our [API Documentation](https://www.klazify.com/category#docs).

Begin leveraging Klazify today to classify any domain or email! Visit [Klazify.com](https://klazify.com) and seamlessly integrate within minutes!

## Installation

You can install Klazify Python SDK with pip.

```bash
pip install klazify
```

## Usage

The Klazify Python SDK is a wrapper around the [requests](https://docs.python-requests.org/en/master/) library. Klazify supports a GET request for now.

Sign-up to Klazify to [get your API key](https://www.klazify.com/register) and some credits to get started.

### Making the GET request

```python
>>> from klazify_api import KlazifyApiClient

>>> client = KlazifyApiClient(access_key='REPLACE-WITH-YOUR-ACCESS-KEY')

>>> response = client.categorize_url("URL")
```

### Request Example

```python
>>> from klazify_api import KlazifyApiClient

>>> client = KlazifyApiClient(access_key='REPLACE-WITH-YOUR-ACCESS-KEY')

>>> response = client.categorize_url("http://razer.com")
```

### Response Example

```json
{
    "domain": {
        "categories": [
            {
                "confidence": 0.62,
                "name": "/Games/Computer & Video Games"
            },
            {
                "confidence": 0.52,
                "name": "/Computers & Electronics/Consumer Electronics"
            }
        ],
        "domain_url": "https://www.razer.com/",
        "social_media": {
            "facebook_url": "https://www.facebook.com/razer",
            "twitter_url": "https://www.twitter.com/Razer",
            "instagram_url": "https://www.instagram.com/razer",
            "medium_url": null,
            "youtube_url": null,
            "pinterest_url": null,
            "linkedin_url": null,
            "github_url": null
        },
        "logo_url": "https://klazify.s3.amazonaws.com/1470029904162279565560b9e587db3951.79673890.png"
    },
    "success": true,
    "objects": {
        "company": {
            "name": "Razer",
            "city": "Irvine",
            "stateCode": "CA",
            "countryCode": "US",
            "employeesRange": "1K-5K",
            "revenue": 1620000000,
            "raised": 110000,
            "tags": [
                "Information Technology & Services",
                "Consumer Electronics",
                "Electronics",
                "Computers",
                "E-commerce",
                "Manufacturing",
                "Software",
                "Publishers",
                "Information",
                "Publishing",
                "Technology",
                "Computer Hardware",
                "B2C",
                "SAAS",
                "Mobile"
            ],
            "tech": [
                "outlook",
                "microsoft_exchange_online",
                "sendgrid",
                "amazon_ses",
                "salesforce",
                "microsoft_office_365",
                "zendesk",
                "cloud_flare",
                "db2",
                "oracle_crm",
                "smartsheet",
                "sybase",
                "apache_kafka",
                "apache_http_server",
                "sap_hybris_marketing",
                "couchbase",
                "dropbox",
                "woo_commerce",
                "flexera_software",
                "oracle_data_integrator",
                "ibm_websphere",
                "sap_concur",
                "rabbitmq",
                "cision",
                "cloudera",
                "apache_hadoop",
                "aws_dynamodb",
                "oracle_weblogic",
                "aws_cloudwatch",
                "atlassian_confluence",
                "sap_crystal_reports",
                "oracle_peoplesoft",
                "apache_tomcat",
                "basecamp",
                "informatica",
                "the_trade_desk",
                "mongodb",
                "microsoft_project",
                "ibm_cognos",
                "pubmatic",
                "workday",
                "peoplesoft_crm",
                "pentaho",
                "sap_sales_order_management",
                "aws_kinesis",
                "apache_spark",
                "sprinklr",
                "qlikview",
                "microsoft_dynamics",
                "aws_redshift",
                "oracle_commerce_cloud",
                "teradata",
                "aws_lambda",
                "google_search_appliance",
                "apache_storm",
                "pivotal_tracker",
                "github",
                "sap_business_objects",
                "sap_hana",
                "quickbooks",
                "netsuite",
                "postgresql",
                "mysql",
                "windows_server",
                "worldpay",
                "servicenow",
                "microsoft_power_bi",
                "sap_crm",
                "atlassian_jira",
                "facebook_workplace",
                "neo4j",
                "hive",
                "filemaker_pro",
                "apache_cassandra",
                "vmware_server"
            ]
        }
    },
    "similar_domains": [
        "logitechg.com",
        "xbox.com",
        "gog.com",
        "secretlab.co",
        "pcgamer.com",
        "mechanicalkeyboards.com",
        "hyperxgaming.com",
        "kinguin.net",
        "scufgaming.com",
        "cdkeys.com"
    ],
    "api_usage": {
        "this_month_api_calls": 679,
        "remaining_api_calls": 1321
    }
}
```

### AVAILABLE METHODS

```python
>>> categorize_url(url: str)
```
