# Auth Module Server Api

## URI

|Method|Uri|Description|
|--|--|--|
|POST|`/auth/register`|Register an unexisting user \*|
|POST|`/auth/login`|Login as an existing user \*|

[\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md#request-body-json)

## Request Header

+ Nothing

## Request Body (JSON)

+ `POST /auth/register`

|Field|Type|Is Required|Description|
|--|--|--|--|
|`username`|`string`|Required|Registered Username|
|`password`|`string`|Required|Registered Password|

Example:

```json
{
    "username": "aaaaaaaa",
    "password": "aaaaaaaa"
} 
```

+ `POST /auth/login`

|Field|Type|Is Required|Description|
|--|--|--|--|
|`username`|`string`|Required|Login Username|
|`password`|`string`|Required|Login Password|
|`expiration`|`int`|Not Required \*|Token Timeout Expiration (second)|

\* Expiration default for 10 minutes

Example:

```json
{
    "username": "aaaaaaaa",
    "password": "aaaaaaaa",
    "expiration": 500
} 
```

## Response Header

+ `POST /auth/login`

|Key|Description|
|--|--|
|`Authorization`|Return User Login Token|

## Response Body (JSON)

+ `POST /auth/login`
+ `POST /auth/register`

|Field|Type|Description|
|--|--|--|
|`username`|`string`|Login Username|
|`message`|`string`|Login Success Or Register Success|

Example:

```json
{
    "username": "aoihosizora",
    "status": "Login Success"
}
```

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Register Error`|(Something wrong with the server)|
|`Login Error`|Password error or use a wrong token|
|`User Exist Error`|Register an exist username|
|`User Not Exist Error`|Login as an unexist username|
|`Username Format Error`|Username length should be in `[5, 30)`|
|`Password Format Error`|Password length should be in `[8, 20)`|