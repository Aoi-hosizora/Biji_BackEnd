# Biji_BackEnd
+ Back-End for [Biji_Baibuti](https://github.com/Aoi-hosizora/Biji_Baibuti) (SCUT Baibuti Project)

### Environment
+ `Flask` 1.0.2
+ `MySQL` 8.0.15
+ `Redis` 3.2.100 for windows
+ `Redis` for linux

### Modules
+ Auth
+ Note, Star, Schedule, Document

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
