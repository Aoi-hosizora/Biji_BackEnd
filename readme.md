# Biji_BackEnd
+ Back-End for [Biji_Baibuti](https://github.com/Aoi-hosizora/Biji_Baibuti) (SCUT Baibuti Project)

### Modules
+ [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)

### Environment
+ `Flask` 1.0.2
+ `MySQL` 8.0.15

### Db Model
```sql
CREATE TABLE TBL_USER (
    USERNAME VARCHAR(30) NOT NULL PRIMARY KEY,
    PASSWORD VARCHAR(120) NOT NULL
);
```
