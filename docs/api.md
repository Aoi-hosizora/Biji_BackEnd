# Biji Public Server Api

## Module API Documents
+ Authorization module see [auth.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md)
+ Note module see [note.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md)
+ Search Star module see [star.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md)
+ Schedule module see [schedule.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md)
+ Document module see [document.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md)
+ Raw static resource url see [raw.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md)

## Revision

|Date|Remark|
|--|--|
|`2019/08/02`|Complete project structure & global error msg|
|`2019/11/16`|Reconstruct the project|

## Common Request Header

+ Routes needed authorization

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User login token (Start with `Bearer`)|

## Common Response Body Format

|Field|Type|Description|
|--|--|--|
|`code`|`int`|Response code|
|`message`|`string`|Response message (error message)|
|`data`|`nullable`|Response Body Data|

+ Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {}
}
```

## Common Status Code

+ See [ResultCode.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/model/dto/ResultCode.py) and [ErrorForward.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/route/ErrorForward.py)

|Code|Message|Description|
|--|--|--|
|600|`Database Failed`|CRUD in database but failed|
|601|`Has Existed`|Insert an existed item into database|
|602|`Duplicate Failed`|Insert or update duplicate into database|
|602|`Default Failed`|Update or delete default item into database|
|603|`Save File Failed`|Save uploaded file to disk failed|

## Common Error Message

+ See [ErrorForward.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/route/ErrorForward.py)

|Code|Message|Description|
|--|--|--|
|200|`Success`||
|400|`Request Param Error`||
|400|`Request Query Param Error`||
|400|`Request Route Param Error`||
|400|`Request Form Data Param Error`||
|400|`Request Raw Json Param Error`||
|400|`Format Error`||
|401|`Token Expired`||
|401|`Token Bad Signature`||