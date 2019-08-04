-- localhost:3366
-- db: test

-- tbl: tbl_user
-- PASSWORD 加密存储

CREATE TABLE `tbl_user` (
  `USERNAME` varchar(30) NOT NULL,
  `PASSWORD` varchar(120) NOT NULL,
  PRIMARY KEY (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_note

CREATE TABLE `tbl_note` (
  `USERNAME` varchar(30) NOT NULL,
  `ID` int(11) NOT NULL,
  `TITLE` varchar(100) NOT NULL,
  `CONTENT` text,
  `GROUPID` int(11) NOT NULL,
  `CREATE_TIME` datetime NOT NULL,
  `UPDATE_TIME` datetime NOT NULL,
  PRIMARY KEY (`USERNAME`,`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_group

CREATE TABLE `tbl_group` (
  `USERNAME` varchar(30) NOT NULL,
  `ID` int(11) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `GORDER` int(11) NOT NULL,
  `COLOR` varchar(10) NOT NULL,
  PRIMARY KEY (`USERNAME`,`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_star

CREATE TABLE `tbl_star` (
  `USERNAME` varchar(30) NOT NULL,
  `TITLE` varchar(100) NOT NULL,
  `URL` varchar(200) NOT NULL,
  `CONTENT` varchar(200) NOT NULL,
  PRIMARY KEY (`USERNAME`,`URL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_file

CREATE TABLE `tbl_file` (
  `USERNAME` varchar(30) NOT NULL,
  `FOLDERNAME` varchar(200) NOT NULL,
  `FILENAME` varchar(200) NOT NULL,
  `FILEPATH` varchar(2000) NOT NULL,
  PRIMARY KEY (`USERNAME`,`FOLDERNAME`,`FILENAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_schedule

CREATE TABLE `tbl_schedule` (
  `USERNAME` varchar(30) NOT NULL,
  `SCHEDULE` varchar(5000) NOT NULL,
  PRIMARY KEY (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- tbl: tbl_log

CREATE TABLE `tbl_log` (
  `USERNAME` varchar(30) NOT NULL,
  `MODULE` varchar(10) NOT NULL,
  `TIME` datetime NOT NULL,
  PRIMARY KEY (`USERNAME`,`MODULE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8