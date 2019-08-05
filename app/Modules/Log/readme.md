# Log Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/04`|Complete log module|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/log/<string>`|Get user module log|
|`GET`|`/log/all`|Get user all logs|
|`POST`|`/log/update`|Update user module log \*|

[\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Log/readme.md#request-body)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ Nothing

## Request Body

+ `POST /log/update`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`module`|`int`|Required|Log module|\[Note|Group|Star|File|Schedule\]|
|`ut`|`datetime`|Required|Log update time|Format like `%Y-%m-%d %H:%M:%S`|

## Response Header

+ Nothing

## Response Body

+ `GET /log/<string>`

|Field|Type|Description|Remark|
|--|--|--|--|
|`module`|`string`|Module name||
|`ut`|`string`|Update time|If not ever update, return create time|

Example:

```json
{
    "module": "File",
    "ut": "2019-08-04 20:57:58"
}
```

+ `GET /log/all`
    + Array
    + Content is same as `GET /log/<string:mod>`

+ `POST /log/update`
    + Same as [Request Body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Log/readme.md#request-body)

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Log Not Found Error`|Log module unknown|