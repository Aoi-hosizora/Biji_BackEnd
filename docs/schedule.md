# Schedule Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/04`|Complete schedule module|
|`2019/11/16`|Reconstruct backend|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/schedule/`|获取用户课表 <sup>[4]</sup>|
|`PUT`|`/schedule/`|更新用户课表 <sup>[1] [4]</sup>|
|`DELETE`|`/schedule/`|删除用户课表 <sup>[4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#response-body)

---

## Request Body

+ `PUT /schedule/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`schedule`|`string`|Required|用户课表 Json 字符串||

---

## Response Body

+ `GET /schedule/` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`schedule`|`string`|用户课表 Json 字符串||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "schedule": "{...}"
    }
}
```

+ `DELETE /schedule` (Json)

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {}
}
```

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|404|`Schedule Not Found`||
|600|`Update Schedule Failed`||
|600|`Delete Schedule Failed`||
