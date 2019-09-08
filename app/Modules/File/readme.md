# File Module Server Api

## Revision

|Date|Remark|
|--|--|
|`2019/08/03`|Complete file module|

## URI

|Method|Uri|Description|
|--|--|--|
|`GET`|`/file/all`|Get all files belong to a directory \*|
|`GET`|`/file/download`|Download a file \*|
|`POST`|`/file/upload`|Upload a file \*\*|
|`DELETE`|`/file/delete`|Delete an file \*\*|
|`DELETE`|`/file/delete_all`|Delete all files by class \*\*|
|`POST`|`/file/push`|Push files \*\*|
|`GET`|`/file/get_share`|Get shared files \*|
|`GET`|`/fileclass/all`|Get all file classes|
|`PUT`|`/fileclass/update`|Update a file class \*\*|
|`POST`|`/fileclass/insert`|Insert a file class \*\*|
|`DELETE`|`/fileclass/delete`|Delete a file class \*\*|
|`POST`|`/fileclass/push`|Push file classes \*\*|
|`GET`|`/fileclass/share`|Get share code \*|

[\* Need request query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-query-param)

[\*\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-body)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ `GET` `/file/all?`
+ `GET` `/fileclass/share?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Queried folder name||

+ `GET /file/download?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Queried folder name||
|`filename`|`string`|Required|Queried file name||

+ `GET /file/get_share?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Shared folder name||

## Request Body

+ `POST /file/upload`
+ `DELETE /file/delete`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Folder name||
|`filename`|`string`|Required|File name||

Example:

```json
{
    "foldername": "Math",
    "filename": "Graph.pdf"
}
```

+ `DELETE` `/file/delete_all`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Folder name||

+ `POST` `/file/push`
    + Array
    
|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|File id||
|`foldername`|`string`|Required|Folder name||
|`filename`|`string`|Required|File name||

+ `PUT` `/fileclass/update`
+ `POST` `/fileclass/insert`
+ `DELETE` `/fileclass/delete`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`id`|`int`|Required|File id||
|`name`|`string`|Required|Folder name||

+ `POST` `/fileclass/push`
    + Array
    + Same as `PUT` `/fileclass/update` Request Body


## Response Body

+ `GET` `/file/all`
    + Array

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`||File id|
|`foldername`|`string`|Folder name||
|`filename`|`string`|File name||

Example:

```json
[
    {
        "id": 1,
        "foldername": "Math",
        "filename": "2019080409543794.txt"
    }
]
```
+ `POST` `/file/upload`
+ `DELETE` `/file/delete`
+ `GET` `/get_share`
+ `POST` `/push`
+ `DELETE` `/delete_all`
+ `POST` `/fileclass/push`

|Field|Type|Description|Remark|
|--|--|--|--|
|`message`|`string`|Upload status||
|`detail`|`string`|Filename|New filename|

Example:

```json
{
    "message": "File upload success",
    "detail": "2019080409543794.txt"
}
```

+ `GET /file/download`
    + Send a file
    
+ `PUT` `/fileclass/update`
+ `POST` `/fileclass/insert`
+ `DELETE` `/fileclass/delete`

|Field|Type|Description|Remark|
|--|--|--|--|
|`id`|`int`|File class id||
|`name`|`string`|File class name||

+ `GET` `/fileclass/all`
    + Array
    + Same as `PUT` `/fileclass/update` Response Body
    
+ `GET` `/fileclass/share`
    + Send an image

## Error Message Type

+ Public error code and error message type see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)

|Message|Description|
|--|--|
|`Not Exist Error`|Delete an unexist file|
|`Exist Error`|Insert an exist file|
|`Insert Error`|Insert into database error|
|`Delete Error`|Delete from database error|
|`File Upload Error`|File not exist or upload error|
|`File Type Error`|File type is not supported|
|`File Not Exist Error`|File not exist|
|`File Class Exist Error`|Insert an exist file class|
|`File Class Not Exist Error`|File class not exist|
