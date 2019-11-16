# Note Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/02`|Complete note module|
|`2019/08/03`|Add `ImgBlue`|
|`2019/08/07`|Add `PushNote` and `PushGroup` route|
|`2019/08/09`|Add `DeleteImg` route|
|`2019/11/16`|Reconstruct backend|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/note/`|获取所有的笔记 <sup>[4]</sup>|
|`GET`|`/note/group/:gid`|获取分组为 gid 的笔记 <sup>[2] [4]</sup>|
|`GET`|`/note/:nid`|获取编号为 nid 的笔记 <sup>[2] [4]</sup>|
|`POST`|`/note/`|新建笔记 <sup>[1] [4]</sup>|
|`PUT`|`/note/`|更新笔记 <sup>[1] [4]</sup>|
|`DELETE`|`/note/:nid`|删除笔记 <sup>[2] [4]</sup>|
|`GET`|`/group/`|获取所有笔记分组 <sup>[4]</sup>|
|`GET`|`/group/:gid`|获取编号为 gid 的笔记分组 <sup>[2] [4]</sup>|
|`GET`|`/group/:name`|获取标题为 name 的笔记分组 <sup>[2] [4]</sup>|
|`GET`|`/group/default`|获取默认笔记分组 <sup>[4]</sup>|
|`POST`|`/group/`|新建笔记分组 <sup>[1] [4]</sup>|
|`PUT`|`/group/`|更新笔记分组 <sup>[1] [4]</sup>|
|`DELETE`|`/group/:gid`|删除笔记分组 <sup>[2] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#response-header)

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

+ `GET /note/:nid`
+ `DELETE /note/:nid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`nid`|`int`|Required|笔记编号||

+ `GET /note/group/:gid`
+ `GET /group/:gid`
+ `DELETE /group/:gid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`gid`|`int`|Required|笔记分组编号||

+ `GET /group/:name`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|笔记分组标题|不能为 `default`|

## Request Body

+ `POST /note/` (Raw-Json)
+ `PUT /note/` (Raw-Json)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|笔记编号|`POST` 占位|
|`title`|`string`|Required|笔记标题||
|`content`|`string`|Required|笔记内容||
|`group`|`object`|Required|笔记分组|只会用到 `group.id`|
|`create_time`|`datetime`|Required|笔记创建时间||
|`update_time`|`datetime`|Required|笔记更新时间||

+ `POST /group/` (Raw-Json)
+ `PUT /group/` (Raw-Json)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|笔记分组编号|`POST` 占位|
|`name`|`string`|Required|笔记分组标题||
|`order`|`int`|Required|笔记分组顺序 (0 开始)|`POST` 占位|
|`color`|`string`|Required|笔记分组颜色||

---

## Response Header

|Field|Type|Description|Remark|
|--|--|--|--|

## Response Body

+ `GET /note/` (Array)
+ `GET /note/group/:gid` (Array)
+ `GET /note/:nid` (Json)
+ `POST /note/` (Json)
+ `PUT /note/` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|笔记编号||
|`title`|`string`|笔记标题||
|`content`|`string`|笔记内容||
|`group`|`object`|笔记分组|见 `GET /group`|
|`create_time`|`datetime`|笔记创建时间||
|`update_time`|`datetime`|笔记更新时间||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {}
}
```

+ `GET /group/` (Array)
+ `GET /group/:gid` (Json)
+ `GET /group/:name` (Json)
+ `GET /group/default` (Json)
+ `POST /group` (Json)
+ `PUT /group` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|笔记分组编号||
|`name`|`string`|笔记分组标题||
|`order`|`int`|笔记分组顺序 (0 开始)||
|`color`|`string`|笔记分组颜色||

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
|404|`Note Not Found`||
|500|`Note Existed`||
|500|`Note Insert Failed`||
|500|`Note Update Failed`||
|500|`Note Delete Failed`||
|404|`Group Not Found`||
|500|`Group Existed`||
|500|`Group Name Duplicate`||
|500|`Group Insert Failed`||
|500|`Could Not Update Default Group`||
|500|`Group Update Failed`||
|500|`Could Not Delete Default Group`||
|500|`Group Delete Failed`||
