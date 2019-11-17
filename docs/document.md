# Document Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete file module|
|`2019/11/16`|Reconstruct backend|

## URI

+ `/document`

|Method|Uri|Description|
|--|--|--|
|`GET`|`/document/`|获取所有文档 <sup>[4]</sup>|
|`GET`|`/document/class/:cid`|获取分组为 cid 的所有文档 <sup>[2] [4]</sup>|
|`GET`|`/document/:did`|获取编号为 did 的文档 <sup>[2] [4]</sup>|
|`POST`|`/document/`|新建文档 <sup>[1] [4]</sup>|
|`PUT`|`/document/`|更新文档 <sup>[1] [4]</sup>|
|`DELETE`|`/document/:did`|删除编号为 did 的文档 <sup>[2] [4]</sup>|

+ `/docclass`

|Method|Uri|Description|
|--|--|--|
|`GET`|`/docclass/`|获取所有文档分组 <sup>[4]</sup>|
|`GET`|`/docclass/:cid`|获取编号为 cid 的文档分组 <sup>[2] [4]</sup>|
|`GET`|`/docclass/?name`|获取分组名为 name 的文档分组 <sup>[2] [4]</sup>|
|`GET`|`/docclass/default`|获取默认文档分组 <sup>[4]</sup>|
|`POST`|`/docclass/`|新建文档分组 <sup>[1] [4]</sup>|
|`PUT`|`/docclass/`|更新文档分组 <sup>[1] [4]</sup>|
|`DELETE`|`/docclass/:cid`|删除编号为 cid 的文档分组 <sup>[2] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#response-body)

---

## Request Query Param

+ `GET /docclass/?name`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|文档分组名||

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
|`file`|`file`|Required|上传的文档文件|只支持 `[txt, md, pdf, doc, docx, ppt, pptx, xls, xlsx, zip, rar]` 與 `[jpg, png, jpeg, bmp]`|
|`doc_class_id`|`int`|Required|文档分组编号||

+ `PUT /document/` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|文档编号||
|`filename`|`string`|Required|文档原始文件名|后缀名 `.xxx` 不要超过 `10` 个字符|
|`doc_class_id`|`int`|Required|文档分组编号||

+ `POST /docclass/` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|文档分组名|长度要求在`[1, 30]`|

+ `PUT /docclass/` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|文档分组编号||
|`name`|`string`|Required|文档分组名|长度要求在`[1, 30]`|

---

## Response Body

+ `GET /document/` (Array)
+ `GET /document/class/:cid` (Array)
+ `GET /document/:did` (Json)
+ `POST /document/` (Json)
+ `PUT /document/` (Json)
+ `DELETE /document/:did` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|文档编号||
|`filename`|`int`|文档原始文件名||
|`docClass`|`object`|文档编号|见 `GET /docclass/`|
|`uuid`|`string`|文档 uuid 文件名||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "id": 3,
        "filename": "angular-dev-roadmap.png",
        "docClass": {
            "id": 1,
            "name": "默认分组"
        },
        "uuid": "201911171436542520.png"
    }
}
```

+ `GET /docclass/`
+ `GET /docclass/:cid`
+ `GET /docclass?name`
+ `GET /docclass/default`
+ `POST /docclass/`
+ `PUT /docclass/`
+ `DELETE /docclass/:cid`

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|文档分组编号||
|`name`|`string`|文档分组名||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "id": 1,
        "name": "默认分组"
    }
}
```

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|404|`Document Not Found`||
|601|`Document Existed`||
|600|`Document Insert Failed`||
|600|`Document Update Failed`||
|600|`Document Delete Failed`||
|404|`Document Class Not Found`||
|601|`Document Class Existed`||
|600|`Document Class Insert Failed`||
|600|`Document Class Update Failed`||
|600|`Document Class Delete Failed`||
|602|`Document Class Name Duplicate`||
|602|`Could Not Update Default Document Class`||
|602|`Could Not Delete Default Document Class`||
|400|`File Extension Error`||
|603|`Save Document Failed`||
