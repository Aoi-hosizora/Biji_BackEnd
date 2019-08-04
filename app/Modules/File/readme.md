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

[\* Need request query param](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-query-param)

[\*\* Need request body](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md#request-body)

## Request Header

+ Global

|Key|Is Required|Description|
|--|--|--|
|`Authorization`|Required|User Login Token|

## Request Query Param

+ `GET /file/all?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Queried folder name||

+ `GET /file/download?`

|Field|Type|Is Required|Description|Remark|
|--|--|--|--|--|
|`foldername`|`string`|Required|Queried folder name||
|`filename`|`string`|Required|Queried file name||

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

## Response Body

+ `GET /file/all`

|Field|Type|Description|Remark|
|--|--|--|--|
|`message`|`string`|Upload status||
|`detail`|`string`|Filename|New filename|

Example:

```json
[
    {
        "foldername": "Math",
        "filename": "2019080409543794.txt"
    }
]
```
+ `POST /file/upload`
+ `DELETE /file/delete`

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
|`File Not Exist Error`|File type not exist|