# Public Server Api

## Modules API Document
+ Auth doc see [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)
+ Note doc see [Note](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md)
+ Star doc see [Star](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md)
+ File doc see [File](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md)
+ Schedule doc see [Schedule](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Schedule/readme.md)
+ Log doc see [Log](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Log/readme.md)

## Revision

|Date|Remark|
|--|--|
|`2019/08/02`|Complete project structure & global error msg|


## Log Route


## Status Code

+ Error code see [ErrorUtil.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Utils/ErrorUtil.py)

## Public Error Response

|Field|Type|Description|
|--|--|--|
|`message`|`string`|Error main title|
|`detail`|`string`|Error detail description|

+ Example:

```json
{
    "message": "Body Json Error",
    "detail": "Body: json key-value error, key ['title', 'url'] not found or error"
}
```

## Public Error Message

|Message|Description|
|--|--|
|`Auth Token Error`|Request with a wrong token or no token|
|`Body Form Error`|Request body form-data is wrong|
|`Body Json Error`|Request body raw-json is wrong|
|`Query Param Error`|Request query param is wrong|