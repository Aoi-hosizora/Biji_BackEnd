# Raw Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/11/16`|Reconstruct backend|

## URI

|Method|Uri|Description|
|--|--|--|
|`POST`|`/raw/image`|上传图片 <sup>[1] [4]</sup>|
|`GET`|`/raw/image/:uid/:filename`|获取图片 <sup>[2]</sup>|
|`DELETE`|`/raw/image/`|删除图片 <sup>[1] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#response-header)

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

+ `GET /raw/image/:uid/:filename`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`uid`|`int`|Required|用户 id||
|`filename`|`string`|Required|图片新文件名||

+ `DELETE /raw/image/`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`type`|`string`|Required|||
|`urls`|`string[]`|Required|图片新文件名||

## Request Body

+ `POST /raw/image` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`imge`|`file`|Required|上传的用户图片||
|`type`|`string`|Required|上传图片的类型|候选：`note`|

+ `DELETE /raw/image/` (Raw-Json)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`type`|`string`|Required|上传图片的类型|候选：`note`|
|`urls`|`string[]`|Required|删除的所有图片名||

---

## Response Header

+ `GET /raw/image/:uid/:filename`

|Field|Type|Description|Remark|
|--|--|--|--|
|`Content-Type`|`string`|`image/png`||

## Response Body

+ `POST /raw/image`

|Field|Type|Description|Remark|
|--|--|--|--|
|`filename`|`string`|上传图片的新文件名||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {}
}
```

+ `DELETE /raw/image`

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|删除的图片数||

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
|400|`Upload File Type Error`||
|400|`Not Support Request Upload Type`||
|500|`Image Save Failed`||
|404|`Image Not Found`||
