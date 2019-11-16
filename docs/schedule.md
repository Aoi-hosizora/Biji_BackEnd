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
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/schedule.md#response-header)

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

+ `PUT /schedule/`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`data`|`string`|Required|用户课表指定格式 Json 字符串|直接置于外层 Json 的 `data`|

---

## Response Header

|Field|Type|Description|Remark|
|--|--|--|--|

## Response Body

+ `GET /schedule/`

|Field|Type|Description|Remark|
|--|--|--|--|
|`data`|`string`|用户课表 Json|直接置于外层 Json 的 `data`|

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|404|`Schedule Not Found`||
|500|`Update Schedule Failed`||
|500|`Delete Schedule Failed`||
