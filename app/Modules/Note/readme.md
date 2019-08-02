# Note Module Server Api

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/note/all`|Get user all notes|
|`GET`|`/note/one`|Get user one notes \*|
|`POST`|`/note/update`|Update note content \*\*|
|`PUT`|`/note/insert`|Add a new note \*\*|
|`DELETE`|`/note/delete`|Delete an old note \*\*|
|`GET`|`/group/all`|Get user all groups|
|`GET`|`/group/one`|Get user one groups \*|
|`POST`|`/group/update`|Update group content \*\*|
|`PUT`|`/group/insert`|Add a new group \*\*|
|`DELETE`|`/group/delete`|Delete an old group \*\*|

[\* Need request query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md#request-query-param)

[\*\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md#request-body-json)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ `GET /note/all?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|Queried note id||

+ `GET /group/all?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|Queried group id||

## Request Body (JSON)

+ `POST /note/update`
+ `PUT /note/insert`
+ `DELETE /note/delete`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|Note ID|Primary key|
|`title`|`string`|Required|Note Title|Max length 100|
|`content`|`string`|Not Required|Note Content||
|`group_id`|`int`|Required|Note Group||
|`create_time`|`datetime`|Required|Note Create Time|Format like `%Y-%m-%d %H:%M:%S`|
|`update_time`|`datetime`|Required|Note Update Time|Format like `%Y-%m-%d %H:%M:%S`|

Example:

```json
{
    "id": 1,
    "title": "New Title",
    "content": "New Content",
    "group_id": 1,
    "create_time": "2019-08-02 17:00:00",
    "update_time": "2019-08-02 17:00:00"
}
```

+ `POST /group/update`
+ `PUT /group/insert`
+ `DELETE /group/delete`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|Group ID|Primary|
|`name`|`string`|Required|Group Name|Max length 100|
|`order`|`int`|Required|Group Order||
|`color`|`int`|Required|Group Color|Fromat like `#FFFFFF`|

Example:

```json
{
    "id": 1,
    "name": "G1",
    "order": 1,
    "color": "#FFFFFF"
}
```

## Response Header

+ Nothing

## Response Body (JSON)

+ `GET /note/all`
+ `GET /group/all`
    + Array
    + Content is same as [request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md#request-body-json)

+ Others (Include `/note` and `/group`)
    + Same as [request Body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md#request-body-json)

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Not Exist Error`|Delete/Update a unexist note or group|
|`Exist Error`|Insert an exist note or group|
|`Insert Error`|Insert into database error|
|`Update Error`|Update database error|
|`Delete Error`|Delete from database error|