# Star Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete star module|
|`2019/08/07`|Add `PushStar` route|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/star/all`|Get user all stars|
|`PUT`|`/star/insert`|Add a new star \*|
|`DELETE`|`/star/delete`|Delete an old star \*|
|`POST`|`/star/push`|Through log update stars \*\*|

[\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md#request-body)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ Nothing

## Request Body

+ `PUT /star/insert`
+ `DELETE /star/delete`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`title`|`string`|Required|Star Item Title|Max length 100|
|`url`|`string`|Required|Star Item URL|Max length 200, primary key|
|`content`|`string`|Not Required|Star Item Content|Max length 300|

Example:

```json
{
    "title": "TITLE",
    "url": "URL",
    "content": "CONTENT"
}
```

+ `POST /star/push`
    + Array
    + Same with `PUT /star/insert` Request Body

## Response Header

+ Nothing

## Response Body

+ `GET /star/all`
    + Array
    + Content is same as [request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md#request-body)

+ `PUT /star/insert`
+ `DELETE /star/delete`
    + Content is same as [request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md#request-body)

+ `POST /star/push`

|Field|Type|Description|Remark|
|--|--|--|--|
|`message`|`string`|Push status||
|`detail`|`string`|Push items length||

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Not Exist Error`|Delete/Update an unexist star item|
|`Exist Error`|Insert an exist star item|
|`Insert Error`|Insert a star item into database error|
|`Update Error`|Update a star item database error|
|`Delete Error`|Delete a star item from database error|