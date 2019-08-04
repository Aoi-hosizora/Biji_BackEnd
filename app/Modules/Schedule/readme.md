# Schedule Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/04`|Complete schedule module|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/schedule/download`|Download a schedule|
|`POST`|`/schedule/upload`|Upload a schedule \*\*|
|`DELETE`|`/schedule/delete`|Delete a schedule|
|`PUT`|`/schedule/update`|Update a schedule \*\*|


[\* Need request query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-query-param)

[\*\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-body)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ Nothing

## Request Body

+ `POST /schedule/upload`
+ `DELETE /schedule/update`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`schedulejson`|`string`|Required|Schedule json string||

Example:

```json
{
    "schedulejson": "[{\"name\": \"Math\", \"teacher\": \"Han Meimei\", \"Room\": \"A2302\", \"day\": 3, \"time\": \"理论：48 实验：16\", \"weeklist\": [1, 2, 3, 4, 5], \"id\": 2, \"start\": 3, \"step\": 2}]"
}
```

## Response Body

+ `GET /schedule/download`
    + Same as [request Body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Schedule/readme.md#request-body)

+ `POST /schedule/upload`
+ `DELETE /schedule/delete`
+ `PUT /schedule/update`

|Field|Type|Description|Remark|
|--|--|--|--|
|`message`|`string`|Upload status||

Example:

```json
{
    "message": "Schedule upload success"
}
```

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Not Exist Error`|Delete an unexist schedule|
|`Exist Error`|Insert an exist schedule|
|`Insert Error`|Insert into database error|
|`Delete Error`|Delete from database error|
|`Update Error`|Update from database error|
|`Schedule Upload Error`|Schedule not exist or upload error|