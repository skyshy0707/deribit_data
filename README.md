# Design decisions

To load currency data this project uses deribit api endpoint[https://docs.deribit.com/api-reference/market-data/public-get_index_chart_data] `public/get_index_chart_data`. As i did ivestigated at this moment no one of deribit endpoints provide currency price which supported in this project for more period than 2 days with accuracy less or equal 60 seconds. Data is updated every 60 seconds in my service. Comparing what time passed since last saved price data every 60 seconds our serice monitors is need to load next changes price for currencies or not.

This endpoint allow to load currency price for last 2 days, so if broker falls and idle more than 2 days data are loss since last time 
is available.

Suppoted currencies: `btc_usd`, `eth_usd`.

# API

<h4>Prefix: /api - for all endpoints<h4>

##

**Get price**

<code style="color : green">GET</code> /info 

```Request```

###### &nbsp;parameters:

&nbsp;&nbsp;&nbsp;ticker: `<str>` Possible values: `btc_usd`, `eth_usd`

&nbsp;&nbsp;&nbsp;timestamp: `<str>` optional, default current UTC time

`timestamp` should be dateformat in ISO string or you can use some approachs of writing date formants described in ГОСТ Р 7.0.97-2016:

`DD.MM.YYYY`

`DD.MM.YYYY.HH:mm`

`D` - day,
`M` - mouth,
`Y` - year,
`H` - hour,
`m` - minutes



```Response``` HTTP Status 200:

JSON*:

```json
{
    "price": <float>,
    "timestamp": <datetime>,
    "currency": <str>
}
```

\* `timestanp` will be in ISO format, `currencry` will be the requested ticker


-------------------------
**Possible HTTP Errors:**

**Doesn't exist**

Occurs if price data not exist by these params `ticker`, `timestamp`

Status code 404

```json
{
    "detail":  "Not found. Detail: Data are not exist for this instrument: `<ticker>` or at this time: `<timestamp>`"
}
```

-------------------------
-------------------------
**Get historical prices**

<code style="color : green">GET</code> /info 

```Request```

###### &nbsp;parameters:

&nbsp;&nbsp;&nbsp;ticker: `<str>`
&nbsp;&nbsp;&nbsp;limit: `<int>` optional, default 10
&nbsp;&nbsp;&nbsp;offset: `<int>` optional, default 0

```Response``` HTTP Status 200:

JSON*: 

```json
{
    "ticker": <str>,
    "data": {
        "limit": <int>,
        "offset": <int>,
        "items": [
            <Price item>,
            ...
        ],
        "total": <int>
    }
}
```

\* Response body property `data` will be:

`limit`, `offset`, `ticker` in the response body are the same values as they were setted in request params,

`total` - total objects of historical prices for this requested `ticker`,

`items` is the list of historical prices as objects for this financial instrument `ticker` by pagination params `limit`, `offset`,

`Price item` has next structure:

```json
{
    "price": <float>,
    "timestamp": <datetime>
}
```

These properties are the same as they described for `Get price` endpoint response


---------
---------
## Build:

```bash
docker compose up -d --build
```

Run tests:

Ensure that the server is running, and you can run tests.

```bash
docker exec -it server pytest ./tests.py 
```