# Biji_BackEnd
+ Back-End for [Biji_Baibuti](https://github.com/Aoi-hosizora/Biji_Baibuti) (SCUT Baibuti Project)
+ Use `uwsgi` + `nginx` + `Flask` + `Blueprint`

### Environment
+ `Flask` 1.0.2
+ `MySQL` 8.0.15
+ `Redis` 3.2.100 for windows
+ `Redis` for linux

### Modules
+ Auth, Note, Star, Schedule, Document, Raw
+ Api see [api.md](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/docs/api.md)
+ Database models see [Model.sql](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/database/Model.sql)

### Run

```bash
# Modify config in ./app/config/Config.py
# Create Database db_biji

python3 ./server.py
```

### Dependency Libraries
+ [pymysql](https://github.com/PyMySQL/PyMySQL)
+ [itsdangerous](https://pythonhosted.org/itsdangerous/)
+ [passlib](https://passlib.readthedocs.io/en/stable/)
+ [werkzeug](https://palletsprojects.com/p/werkzeug/)
+ [flask-httpauth](https://flask-httpauth.readthedocs.io/en/latest/)
