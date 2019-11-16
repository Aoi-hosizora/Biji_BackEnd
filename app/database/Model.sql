-- localhost:3306
-- db: db_biji

-- tbl: tbl_user

CREATE TABLE `tbl_user`
(
    `u_id`       int(11)      NOT NULL AUTO_INCREMENT,
    `u_name`     varchar(30)  NOT NULL,
    `u_password` varchar(150) NOT NULL,
    PRIMARY KEY (`u_id`),
    UNIQUE KEY `u_name` (`u_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_note

CREATE TABLE `tbl_note`
(
    `n_user`        int(11)     NOT NULL,
    `n_id`          int(11)     NOT NULL AUTO_INCREMENT,
    `n_title`       varchar(50) NOT NULL,
    `n_content`     text,
    `n_group_id`    int(11)     NOT NULL,
    `n_create_time` datetime    NOT NULL,
    `n_update_time` datetime    NOT NULL,
    PRIMARY KEY (`n_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_group

CREATE TABLE `tbl_group`
(
    `g_user`  int(11)     NOT NULL,
    `g_id`    int(11)     NOT NULL AUTO_INCREMENT,
    `g_name`  varchar(30) NOT NULL,
    `g_order` int(11)     NOT NULL,
    `g_color` varchar(10) NOT NULL,
    PRIMARY KEY (`g_id`),
    UNIQUE KEY `g_name` (`g_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_star

CREATE TABLE `tbl_star`
(
    `sis_user`    int(11)      NOT NULL,
    `sis_id`      int(11)      NOT NULL AUTO_INCREMENT,
    `sis_url`     varchar(500) NOT NULL,
    `sis_title`   varchar(100) NOT NULL,
    `sis_content` varchar(200) DEFAULT NULL,
    PRIMARY KEY (`sis_id`),
    UNIQUE KEY `sis_url` (`sis_url`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_schedule

CREATE TABLE `tbl_schedule`
(
    `sc_user` int(11) NOT NULL,
    `sc_json` text DEFAULT (_utf8mb3''),
    PRIMARY KEY (`sc_user`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_document

CREATE TABLE `tbl_document`
(
    `d_user`      int(11)     NOT NULL,
    `d_id`        int(11)     NOT NULL AUTO_INCREMENT,
    `d_filename`  text        NOT NULL,
    `d_uuid_name` varchar(28) NOT NULL,
    `d_class_id`  int(11)     NOT NULL,
    PRIMARY KEY (`d_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- tbl: tbl_docclass

CREATE TABLE `tbl_doc_class`
(
    `dc_user` int(11)     NOT NULL,
    `dc_id`   int(11)     NOT NULL AUTO_INCREMENT,
    `dc_name` varchar(30) NOT NULL,
    PRIMARY KEY (`dc_id`),
    UNIQUE KEY `dc_name` (`dc_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
