# File Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete file module|
|`2019/11/16`|Reconstruct backend|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/document/`|获取所有文档 <sup>[4]</sup>|
|`GET`|`/document/class/:cid`|获取分组为 cid 的所有文档 <sup>[2] [4]</sup>|
|`GET`|`/document/:did`|获取编号为 did 的文档 <sup>[2] [4]</sup>|
|`POST`|`/document/`|新建文档 <sup>[1] [4]</sup>|
|`PUT`|`/document/`|更新文档 <sup>[1] [4]</sup>|
|`DELETE`|`/document/:did`|删除编号为 did 的文档 <sup>[2] [4]</sup>|
|`GET`|`/docclass/`|获取所有文档分组 <sup>[4]</sup>|
|`GET`|`/docclass/:cid`|获取编号为 cid 的文档分组 <sup>[2] [4]</sup>|
|`GET`|`/docclass/default`|获取默认文档分组 <sup>[4]</sup>|
|`POST`|`/docclass/`|新建文档分组 <sup>[1] [4]</sup>|
|`PUT`|`/docclass/`|更新文档分组 <sup>[1] [4]</sup>|
|`DELETE`|`/docclass/:cid`|删除编号为 cid 的文档分组 <sup>[2] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#response-header)

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

+ `GET /document/:did`
+ `DELETE /document/:did`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`did`|`int`|Required|查询或删除的文档编号||

+ `GET /document/class/:cid`
+ `GET /docclass/:cid`
+ `DELETE /docclass/:cid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`cid`|`int`|Required|文档分组编号||

## Request Body

+ `POST /document/` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`file`|`file`|Required|上传的文档文件||
|`filename`|`string`|Required|文档原始文件名||
|`docClass`|`int`|Required|文档归档编号||

+ `PUT /document/` (Raw-Json)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|文档编号||
|`filename`|`string`|Required|文档原始文件名||
|`docClass`|`object`|Required|文档归档分组|见 `GET /document/class`|

<!-- |`server_filename`|`string`|Required|文档 uuid 名|`PUT` 占位| -->

+ `POST /docclass/` (Raw-Json)
+ `PUT /docclass/` (Raw-Json)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|文档分组编号|`POST` 占位|
|`name`|`string`|Required|文档分组名||

---

## Response Header

|Field|Type|Description|Remark|
|--|--|--|--|

## Response Body

+ `GET /document/` (Array)
+ `GET /document/class/:cid` (Array)
+ `GET /document/:did` (Json)
+ `POST /document/` (Json)
+ `PUT /document/` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|文档编号||
|`filename`|`int`|文档原始文件名||
|`docClass`|`object`|文档编号|见 `GET /docclass/`|
|`server_filename`|`string`|文档 uuid 文件名||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {}
}
```

+ `GET /docclass/`
+ `GET /docclass/:cid`
+ `GET /docclass/default`
+ `POST /docclass/`
+ `PUT /docclass/`

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|文档分组编号||
|`name`|`string`|文档分组名||

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
|404|`Document Not Found`||
|400|`Upload File Type Error`||
|500|`Document Existed`||
|500|`Document Insert Failed`||
|500|`Document Update Failed`||
|500|`Document Delete Failed`||
|404|`Document Class Not Found`||
|500|`Document Class Existed`||
|500|`Document Class Name Duplicate`||
|500|`Document Class Insert Failed`||
|500|`Could Not Update Default Document Class`||
|500|`Document Class Update Failed`||
|500|`Could Not Delete Default Document Class`||
|500|`Document Class Delete Failed`||
