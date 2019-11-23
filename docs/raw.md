# Raw Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Add `ImgBlue`|
|`2019/11/16`|Reconstruct backend|
|`2019/11/21`|Adjust `POST /raw/image` response body|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/raw/image/:uid/:filename`|获取图片 <sup>[2]</sup>|
|`POST`|`/raw/image`|上传图片 <sup>[1] [4]</sup>|
|`DELETE`|`/raw/image/`|删除图片 <sup>[1] [4]</sup>|
|`GET`|`/raw/file/:uuid`|获取文件 <sup>[2] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/raw.md#response-body)

---

## Request Route Param

+ `GET /raw/image/:uid/:filename`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`uid`|`int`|Required|用户 id||
|`filename`|`string`|Required|图片新文件名||

+ `GET /raw/file/:uuid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`uuid`|`int`|Required|文件的标识符 (在服务器的保存名)|需要和用户对应，否则会返回 `Not Found`|

## Request Body

+ `POST /raw/image` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`imge`|`file`|Required|上传的用户图片|只支持 `[jpg, png, jpeg, bmp]`|
|`type`|`string`|Required|上传图片的类型|候选：`note`|

+ `DELETE /raw/image/` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`urls`|`string[]`|Required|删除的所有图片名||
|`type`|`string`|Required|上传图片的类型|候选：`note`|

---

## Response Body

+ `POST /raw/image`

|Field|Type|Description|Remark|
|--|--|--|--|
|`filename`|`string`|上传图片的新路径名||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "filename": "/raw/image/5/201911171451307609.png"
    }
}
```

+ `DELETE /raw/image` (停用)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|删除的图片数量||

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
|404|`Image Not Found`|图片找不到|
|400|`File Extension Error`||
|400|`Not Support Upload Type`||
|603|`Save Image Failed`||
|404|`File Not Found`|文件找不到|
