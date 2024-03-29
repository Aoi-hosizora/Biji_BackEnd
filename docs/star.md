# Star Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete star module|
|`2019/08/07`|Add `PushStar` route|
|`2019/11/16`|Reconstruct backend|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/star/`|获取所有收藏 <sup>[4]</sup>|
|`GET`|`/star/:sid`|获取编号为 sid 的收藏 <sup>[2] [4]</sup>|
|`POST`|`/star/`|添加收藏 <sup>[1] [4]</sup>|
|`DELETE`|`/star/:sid`|删除收藏 <sup>[2] [4]</sup>|
|`DELETE`|`/star/`|删除多个收藏 <sup>[1] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/star.md#response-body)

---

## Request Route Param

+ `GET /star/:sid`
+ `DELETE /star/:sid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`sid`|`int`|Required|查询或删除的收藏 id||

## Request Body

+ `POST /star/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`title`|`string`|Required|收藏项标题|长度超过`[1, 100]`自动截断|
|`url`|`string`|Required|收藏项链接||
|`content`|`string`|Required|收藏项内容|长度超过`[1, 200]`自动截断|

+ `DELETE /star/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int[]`|Required|删除的所有收藏编号||

---

## Response Body

+ `GET /star/` (Array)
+ `GET /star/:sid` (Json)
+ `POST /star/` (Json)
+ `DELETE /star/:sid` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|收藏项编号||
|`title`|`string`|收藏项标题||
|`url`|`string`|收藏项链接||
|`content`|`string`|收藏项内容||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": [
        {
            "id": 1,
            "title": "Test",
            "url": "http://xxx",
            "content": ""
        }
    ]
}
```

+ `DELETE /star/` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|删除的项数||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "count": 3
    }
}
```

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|404|`StarItem Not Found`||
|601|`StarItem Existed`||
|600|`StarItem Insert Failed`||
|600|`StarItem Delete Failed`||
|602|`StarItem Url Duplicate`||
