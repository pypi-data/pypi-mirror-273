# [![Metals-API](https://www.metals-api.com/assets/images/brand/icon-with-text.png)](https://metals-api.com)

**Metals-API Python SDK** - The ultimate API for accessing precious metals spot prices and historical data effortlessly.
Explore real-time and historical metal rates with exceptional accuracy.

## Key Features:

- **Built for Developers:** Tailored for developers, ensuring ease of use and seamless integration.
- **Powerful JSON API:** Robust JSON API designed for accurate and efficient data retrieval.
- **Bank-Level Security:** Trust Metals-API with top-tier security measures to safeguard your data.
- **Reliable Data Sources:** Benefit from reliable and accurate data derived from trusted sources.
- **Flexible Integration:** Easily integrate Metals-API into any language, making it adaptable for diverse applications.
- **Historical Data Access:** Dive into historical data for comprehensive analysis and informed decision-making.
- **Exceptional Accuracy:** Rely on Metals-API for spot-on accuracy in real-time and historical data.
- **User-Friendly Documentation:** Navigate through our comprehensive documentation for a smooth integration process.
- **Specialized Support:** Count on our dedicated support team for assistance tailored to your specific needs.

## Supported Symbols

Explore a wide range of supported symbols, including gold, silver, platinum, palladium, and various others. From LBMA Gold to LME Steel, we cover it all. [View Symbols](https://www.metals-api.com/symbols)

## Available Endpoints

The Metals-API API comes with multiple endpoints, each providing different functionality. However, in this section, we will focus on the Latest Rates endpoint, Historical Rates and Times Series

1. **Latest Rates Endpoint**
   - Returns real-time exchange rate data for all available or a specific set of currencies. (The number of symbols per API request depends on the acquired plan).

2. **Historical Rates Endpoint**
   - Returns historical exchange rate data for a specific set of currencies. (The number of symbols per API request depends on the acquired plan).

3. **Time-Series Data Endpoint**
   - Returns daily historical exchange rate data between two specified dates for all available or a specific set of currencies. (The date limits per API request depend on the acquired plan).

## Documentation

For detailed information on API endpoints, usage, and integration guidelines, check our [API Documentation](https://www.metals-api.com/documentation).

Start using Metals-API today for unparalleled access to precious metals data. Visit [Metals-API.com](https://metals-api.com) and integrate in just minutes!


## Installation

You can install Metals-API Python SDK with pip.

```bash
pip metals_api
```

## Usage

The Metals-API Python SDK is a wrapper around the [requests](https://docs.python-requests.org/en/master/) library. Metals-API supports a GET request for now.

Sign-up to Metals-API to [get your API key](https://metals-api.com/register) and some credits to get started.

### Making the GET request

```python
>>> from metals_api import MetalsApiClient

>>> client = MetalsApiClient(access_key='REPLACE-WITH-YOUR-ACCESS-KEY')

>>> response = client.get_latest("base", ["symbols"])
```

### Request Example

```python
>>> from metals_api import MetalsApiClient

>>> client = MetalsApiClient(access_key='REPLACE-WITH-YOUR-ACCESS-KEY')

>>> response = client.get_latest("USD", ["XAU", "XAG", "XPT"])
```

### Response Example

```json
{
    "success": true,
    "timestamp": 1715695200,
    "date": "2024-05-14",
    "base": "USD",
    "rates": {
        "USD": 1,
        "XAG": 0.034989609514923,
        "XAU": 0.00042501745902135,
        "XPT": 0.0009786668257129,
        "USDXAG": 28.579913118878963,
        "USDXAU": 2352.8445214994495,
        "USDXPT": 1021.79819906694
    }
}
```

### AVAILABLE METHODS

```python
>>> get_latest(base: str, symbols: List[str])
```

```python
>>> get_historical(date:str, base:str, symbols: List[str])
```

```python
>>> get_time_series(start_date: str, end_date: str, symbol: str)
```

