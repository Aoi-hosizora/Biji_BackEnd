# Note Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/02`|Complete note module|
|`2019/08/07`|Add `PushNote` and `PushGroup` route|
|`2019/11/16`|Reconstruct backend|
|`2019/11/21`|Adjust `DELETE /docclass/:cid?default` request param|

## URI

+ `/note`

|Method|Uri|Description|
|--|--|--|
|`GET`|`/note/`|获取所有的笔记 <sup>[4]</sup>|
|`GET`|`/note/group/:gid`|获取分组为 gid 的笔记 <sup>[2] [4]</sup>|
|`GET`|`/note/:nid`|获取编号为 nid 的笔记 <sup>[2] [4]</sup>|
|`POST`|`/note/`|新建笔记 <sup>[1] [4]</sup>|
|`PUT`|`/note/`|更新笔记 <sup>[1] [4]</sup>|
|`DELETE`|`/note/:nid`|删除笔记 <sup>[2] [4]</sup>|
|`DELETE`|`/note/`|删除多个笔记 <sup>[1] [4]</sup>|

+ `/group`

|Method|Uri|Description|
|--|--|--|
|`GET`|`/group/`|获取所有笔记分组 <sup>[4]</sup>|
|`GET`|`/group/:gid`|获取编号为 gid 的笔记分组 <sup>[2] [4]</sup>|
|`GET`|`/group/?name`|获取标题为 name 的笔记分组 <sup>[3] [4]</sup>|
|`GET`|`/group/default`|获取默认笔记分组 <sup>[4]</sup>|
|`POST`|`/group/`|新建笔记分组 <sup>[1] [4]</sup>|
|`PUT`|`/group/`|更新笔记分组 <sup>[1] [4]</sup>|
|`PUT`|`/group/order`|更新笔记分组顺序 <sup>[1] [4]</sup>|
|`DELETE`|`/group/:gid?default`|删除笔记分组 <sup>[2] [3] [4]</sup>|

+ [1] [Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-body)
+ [2] [Need route param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-route-param)
+ [3] [Need query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-query-param)
+ [4] [Need login](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#request-header)
+ [Response](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/note.md#response-body)

---

## Request Query Param

+ `GET /group/?name`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|笔记分组名||

+ `DELETE /group/:gid?default`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`default`|`boolean`|Not Required|删除分组时若有关联笔记则修改为默认，否则直接删除笔记|默认为 `false`|

## Request Route Param

+ `GET /note/:nid`
+ `DELETE /note/:nid`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`nid`|`int`|Required|笔记编号||

+ `GET /note/group/:gid`
+ `GET /group/:gid`
+ `DELETE /group/:gid?default`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`gid`|`int`|Required|笔记分组编号||

## Request Body

+ `POST /note/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`title`|`string`|Required|笔记标题|长度要求在`[1, 50]`|
|`content`|`string`|Required|笔记内容||
|`group_id`|`int`|Required|笔记分组||
|`create_time`|`string`|Required|笔记创建时间|格式为 `2019-11-17 11:18:59`|
|`update_time`|`string`|Required|笔记更新时间|同上|

+ `PUT /note/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|笔记编号||
|`title`|`string`|Required|笔记标题|长度要求在`[1, 50]`|
|`content`|`string`|Required|笔记内容||
|`group_id`|`int`|Required|笔记分组||

+ `DELETE /note/` (Form-Data)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int[]`|Required|删除的笔记编号||

+ `POST /group/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`name`|`string`|Required|分组标题|长度要求在`[1, 30]`|
|`color`|`string`|Not Required|分组颜色|默认为 `#A5A5A5`|

+ `PUT /group/` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|分组编号||
|`name`|`string`|Required|分组标题|长度要求在`[1, 30]`|
|`order`|`int`|Required|分组顺序|从0开始|
|`color`|`string`|Not Required|分组颜色|默认为 `#A5A5A5`|

+ `PUT /group/order` (Data-Form)

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id_order`|`string`|Required|分组的编号与新顺序组合|格式为 `id_order`，例如 `3_5`|

---

## Response Body

+ `GET /note/` (Array)
+ `GET /note/group/:gid` (Array)
+ `GET /note/:nid` (Json)
+ `POST /note/` (Json)
+ `PUT /note/` (Json)
+ `DELETE /note/:nid` (Json)

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
    "data": {
        "id": 1,
        "title": "Demo Title",
        "content": "Demo Content",
        "group": {
            "id": 1,
            "name": "默认分组",
            "order": 0,
            "color": "#A5A5A5"
        },
        "create_time": "2019-11-17 11:18:59",
        "update_time": "2019-11-17 11:18:59"
    }
}
```

+ `DELETE /note/` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|多删除的笔记数量||

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

+ `GET /group/` (Array)
+ `GET /group/:gid` (Json)
+ `GET /group/?name` (Json)
+ `GET /group/default` (Json)
+ `POST /group/` (Json)
+ `PUT /group/` (Json)
+ `DELETE /group/:gid` (Json)

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|笔记分组编号||
|`name`|`string`|笔记分组标题||
|`order`|`int`|笔记分组顺序|从0开始|
|`color`|`string`|笔记分组颜色||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "id": 2,
        "name": "Demo",
        "order": 1,
        "color": "#A5A5A5"
    }
}
```

+ `PUT /group/order`

|Field|Type|Description|Remark|
|--|--|--|--|
|`count`|`int`|分组修改的个数||

Example:

```json
{
    "code": 200,
    "message": "Success",
    "data": {
        "count": 2
    }
}
```

---

## Error Message

+ Other public error message see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)

|Code|Message|Description|
|--|--|--|
|404|`Note Not Found`||
|601|`Note Existed`||
|600|`Note Insert Failed`||
|600|`Note Update Failed`||
|600|`Note Delete Failed`||
|404|`Group Not Found`||
|601|`Group Existed`||
|600|`Group Insert Failed`||
|600|`Group Update Failed`||
|600|`Group Delete Failed`||
|602|`Group Name Duplicate`||
|603|`Could Not Update Default Group`||
|603|`Could Not Delete Default Group`||
