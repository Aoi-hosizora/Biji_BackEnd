# Authorization Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/02`|Complete Auth Module|
|`2019/08/07`|Add logout route|
|`2019/11/16`|Reconstruct backend|

---

## URI

|Method|Uri|Description|
|--|--|--|
|`POST`|`/auth/login`|Login <sup>[1]</sup>|
|`POST`|`/auth/register`|Register <sup>[1]</sup>|
|`POST`|`/auth/logout`|Logout <sup>[4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#response-header)

---

## Request Header

+ Routes needed authorization

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User login token (Start with `Bearer`)|

## Request Query Param

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|

## Request Route Param

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|

## Request Body

+ `POST /auth/login` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`username`|`string`|Required|User's username||
|`password`|`string`|Required|User's password||
|`expiration`|`int`|Not required|Login expiration(second)|Default for `1 days`|

+ `POST /auth/register` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`username`|`string`|Required|User's username||
|`password`|`string`|Required|User's password||

---

## Response Header

+ `POST /auth/login`

|Field|Type|Description|Remark|
|--|--|--|--|
|`Authorization`|`string`|User login token|Default expired time is `1 days`|

## Response Body

+ `POST /auth/login` (Json)
+ `POST /auth/register` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|User id||
|`username`|`string`|User name||

Example:
```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "username": "Testuser"
    }
}
```

+ `POST /auth/logout` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|Logout deleted token count||

Example:
```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "count": 1
    }
}
```

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|200|`Success`||
|401|`Password Error`||
|401|`User Not Found`||
|401|`Login Failed`||
|401|`Register Failed`||
|401|`User Existed`||
|500|`Logout Failed`||
