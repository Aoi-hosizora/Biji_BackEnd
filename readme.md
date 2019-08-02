# Biji_BackEnd
+ Back-End for [Biji_Baibuti](https://github.com/Aoi-hosizora/Biji_Baibuti) (SCUT Baibuti Project)

### Modules
+ [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)
+ [Note](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md)
+ [Star](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md)

### Environment
+ `Flask` 1.0.2
+ `MySQL` 8.0.15
+ `Redis` 3.2.100 for windows

### Config
+ See [Config.py](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Config/Config.py)

### Run

```bash
# Modify config in ./app/Config/Config.py
python3 ./listen.py
```

### Structure

```
.
│  listen.py    -> Main Program
├─app           
│  ├─Config     -> Some Config
│  ├─Modules    
│  │  ├─Auth    -> Auth Module
│  │  ├─Note    -> Note Module
│  │  └─Star    -> Star Module
│  └─ ...       
└─usr           -> User Files
    └─img       -> Notes Image
```

### Db Model
+ MySQL Models see [Model.sql](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Database/Model.sql)

### API Document
+ Public doc see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)
+ Auth doc see [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)
+ Note doc see [Note](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md)
+ Star doc see [Star](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md)