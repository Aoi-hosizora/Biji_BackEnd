# Public Server Api

### Status Code

+ Error code see [ErrorUtil.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Utils/ErrorUtil.py)

### Public Error Response

|Field|Type|Description|
|--|--|--|
|`message`|`string`|Error main title|
|`detail`|`string`|Error detail description|

+ Example:

```json
{
    "message": "Login Timeout",
    "detail": "User login timeout"
}
```

### Public Error Message

|Message|Description|
|--|--|
|`Auth Token Error`|Request with a wrong token or no token|
|`Body Form Error`|Request body form-data is wrong|
|`Body Json Error`|Request body raw-json is wrong|
|`Query Param Error`|Request query param is wrong|