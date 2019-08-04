# Log Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/04`|Complete log module|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/log/<string:mod>`|Get user `mod` module log|
|`GET`|`/log/all`|Get user all logs|

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ Nothing

## Request Body

+ Nothing

## Response Header

+ Nothing

## Response Body

+ `GET /log/<string:mod>`

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

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Log Not Found Error`|Log type unknown|