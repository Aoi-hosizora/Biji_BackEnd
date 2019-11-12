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

### Structure
```
.
├── app
│   ├── Config        -> Some Config
│   ├── Modules
│   │   ├── Auth      -> Auth Module
│   │   ├── File      -> File Module
│   │   ├── Log       -> Log Module
│   │   ├── Note      -> Note Module
│   │   ├── Schedule  -> Schedule Module
│   │   └── Star      -> Star Module
│   └── ...
├── listen.py         -> Main Program
└── usr               -> User Directory
    ├── file          -> User Files
    └── img           -> Notes Image
```

### Db Model
+ MySQL Models see [Model.sql](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Database/Model.sql)

### API Document
+ Public doc see [Modules](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/readme.md)
+ Auth doc see [Auth](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Auth/readme.md)
+ Note doc see [Note](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Note/readme.md)
+ Star doc see [Star](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Star/readme.md)
+ File doc see [File](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/File/readme.md)
+ Schedule doc see [Schedule](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Modules/Schedule/readme.md)
+ Log doc see [Log](https://github.com/Aoi-hosizora/Biji_BackEnd/blob/master/app/Log/Schedule/readme.md)