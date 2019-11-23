# Document Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete file module|
|`2019/11/18`|Reconstruct backend|
|`2019/11/21`|Adjust `DELETE /docclass/:cid?default` request param|

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
|`GET`|`/docclass?name`|获取分组名为 name 的文档分组 <sup>[2] [4]</sup>|
|`GET`|`/docclass/default`|获取默认文档分组 <sup>[4]</sup>|
|`POST`|`/docclass/`|新建文档分组 <sup>[1] [4]</sup>|
|`PUT`|`/docclass/`|更新文档分组 <sup>[1] [4]</sup>|
|`DELETE`|`/docclass/:cid?default`|删除编号为 cid 的文档分组 <sup>[2] [3] [4]</sup>|

+ `/share`

|Method|Uri|Description|
|--|--|--|
|`GET`|`/share/`|获得用户所有的共享文档与共享码 <sup>[4]</sup>|
|`POST`|`/share/`|设置指定的文档为共享文档 <sup>[1] [4]</sup>|
|`POST`|`/share?cid`|设置指定分组的所有文档为共享文档 <sup>[1] [3] [4]</sup>|
|`DELETE`|`/share/`|删除共享码 <sup>[1] [4]</sup>|
|`DELETE`|`/share/user`|删除用户所有共享码 <sup>[4]</sup>|
|`GET`|`/share/:sc`|根据共享码获取文档 <sup>[2]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/document.md#response-body)

---

## Request Query Param

+ `GET /docclass?name`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|文档分组名||

+ `DELETE /docclass/:gid?default`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`default`|`boolean`|Not Required|删除分组时若有关联文档则修改为默认，否则删除记录与文件|默认为 `false`|

+ `POST /share?cid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`cid`|`int`|Required|指定整个分组共享的分组编号||

## Request Route Param

+ `GET /document/:did`
+ `DELETE /document/:did?default`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`did`|`int`|Required|查询或删除的文档编号||

+ `GET /document/class/:cid`
+ `GET /docclass/:cid`
+ `DELETE /docclass/:cid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`cid`|`int`|Required|文档分组编号||

+ `PUT /share/:sc`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`sc`|`string`|Required|文档共享码||

## Request Body

+ `POST /document/` (Form-data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`file`|`file`|Required|上传的文档文件|只支持 `[txt, md, pdf, doc, docx, ppt, pptx, xls, xlsx, zip, rar]` 与 `[jpg, png, jpeg, bmp]`，并且文件大小限制在 `50MB` 以内|
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

+ `POST /share/` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`ex`|`int`|Not Required|共享时间长度|单位为秒，默认为一个小时 (3600s)|
|`did`|`int[]`|Required|共享的用户文档编号|非该用户的文档自动忽略|

+ `POST /share?cid` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`ex`|`int`|Not Required|共享时间长度|单位为秒，默认为一个小时 (3600s)|

+ `DELETE /share/` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`sc`|`string[]`|Required|删除的所有共享码||

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

+ `GET /share/` (Array)
+ `POST /share/` (Json)
+ `POST /share?cid` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`sc`|`string`|用户的一个文档共享码||
|`documents`|`Document[]`|该共享码的所有文档|格式见 `GET /document/`|

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "sc": "biji_sc_1_2019112000075599",
        "documents": [{
            "id": 7,
            "filename": "可伸缩服务架构：框架与中间件.pdf",
            "docClass": {
                "id": 5,
                "name": "Demos"
            },
            "uuid": "201911192218313716.png"
        }]
    }
}
```

+ `DELETE /share/` (Json)
+ `DELETE /share/user` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|删除的共享码个数||

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
|603|`Could Not Update Default Document Class`||
|603|`Could Not Delete Default Document Class`||
|400|`File Extension Error`|文件的后缀名不受支持|
|400|`File Out Of Size`|文件超过大小限制|
|604|`Save Document Failed`||
|605|`Share Documents Null`|共享的文档集合为空|
|600|`Document Share Code Generate Failed`||
|400|`Share Code Illegal`|共享码不合法|
|400|`Share Code Not Exist`|共享码不存在 (可能过期)|
|605|`Share Code Not Include File`|共享码不包含文件|
|404|`File Not Found`|共享码包含单个文件不存在|
|500|`Zip File Generate Failed`|生成压缩包错误|

