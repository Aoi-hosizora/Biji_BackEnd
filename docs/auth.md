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
|`GET`|`/auth/`|获取当前登录用户信息 <sup>[4]</sup>|
|`POST`|`/auth/login`|登录 <sup>[1]</sup>|
|`POST`|`/auth/register`|注册 <sup>[1]</sup>|
|`POST`|`/auth/logout`|注销 <sup>[4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/auth.md#response-body)

---

## Request Body

+ `POST /auth/login` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`username`|`string`|Required|用户名||
|`password`|`string`|Required|密码||
|`expiration`|`int`|Not required|登陆有效期(单位秒)|默认为一天|

+ `POST /auth/register` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`username`|`string`|Required|用户名|长度要求在`[5, 30]`|
|`password`|`string`|Required|密码|长度要求在`[8, 20]`|

---

## Response Header

+ `POST /auth/login`

|Field|Type|Description|Remark|
|--|--|--|--|
|`Authorization`|`string`|用户登陆令牌|默认有效期是一天|

## Response Body

+ `GET /auth/` (Json)
+ `POST /auth/login` (Json)
+ `POST /auth/register` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|用户 id||
|`username`|`string`|用户名||

Example:
```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "username": "aoihosizora"
    }
}
```

+ `POST /auth/logout` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|当前注销操作删除的令牌数||

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
|600|`Logout Failed`||
