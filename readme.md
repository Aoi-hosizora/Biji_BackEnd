# Biji_BackEnd
+ Back-End for [Biji_Baibuti](https://github.com/Aoi-hosizora/Biji_Baibuti) (SCUT Baibuti Project)

### Modules
+ [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)
+ [Note](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md)
+ [Star](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md)
+ [File](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md)
+ [Schedule](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Schedule/readme.md)
+ [Log](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Log/readme.md)

### Environment
+ `Flask` 1.0.2
+ `MySQL` 8.0.15
+ `Redis` 3.2.100 for windows
+ `Redis` for linux

### Config
+ See [Config.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Config/Config.py)

### Run

```bash
# Modify config in ./app/config/Config.py
python3 ./server.py
```

### Database Models
+ MySQL database Models see [Model.sql](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Database/Model.sql)

### Dependency Libraries
+ [pymysql](https://github.com/PyMySQL/PyMySQL)
+ [itsdangerous](https://pythonhosted.org/itsdangerous/)
+ [passlib](https://passlib.readthedocs.io/en/stable/)
+ [werkzeug](https://palletsprojects.com/p/werkzeug/)
+ [flask-httpauth](https://flask-httpauth.readthedocs.io/en/latest/)
