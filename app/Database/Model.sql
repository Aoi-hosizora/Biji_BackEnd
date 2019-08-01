-- localhost:3366
-- db: test
-- tbl: tbl_user

CREATE TABLE `tbl_user` (
  `USERNAME` varchar(30) NOT NULL,
  `PASSWORD` varchar(120) NOT NULL,
  PRIMARY KEY (`USERNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

-- PASSWORD 加密存储