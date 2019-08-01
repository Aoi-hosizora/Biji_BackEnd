# Auth Module Server Api

### URI

|Method|Uri|Description|
|--|--|--|
|POST|`/auth/register`|Register an unexisting user|
|POST|`/auth/login`|Login as an existing user|

### Request Header

+ Nothing

### Request Body (JSON)

+ `POST /auth/register`

|Field|Type|Is Required|Description|
|--|--|--|--|
|`username`|`string`|Required|Registered Username|
|`password`|`string`|Required|Registered Password|

+ `POST /auth/login`

|Field|Type|Is Required|Description|
|--|--|--|--|
|`username`|`string`|Required|Login Username|
|`password`|`string`|Required|Login Password|
|`expiration`|`int`|Not Required \*|Token Timeout Expiration|

\* Expiration default for 10 minutes

### Response Header

+ `POST /auth/login`

|Key|Description|
|--|--|
|Authorization|Return User Login Token|

### Response Body (JSON)

+ `POST /auth/login`
+ `POST /auth/register`

|Field|Type|Description|
|--|--|--|
|`username`|`string`|Login Username|
|`message`|`string`|Login Success Or Register Success|

### Public Status Code

+ Error Code See [ErrorUtil.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Utils/ErrorUtil.py) and [ErrorHandler.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/Routes/ErrorHandler.py)

### Error Message

|Field|Type|Description|
|--|--|--|
|`message`|`string`|Error Main Title|
|`detail`|`string`|Error Description|
