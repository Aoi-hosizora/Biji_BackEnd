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