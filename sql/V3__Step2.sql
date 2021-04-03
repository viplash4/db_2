CREATE TABLE PersonInfo
(
    OUTID            character varying(255) PRIMARY KEY,
    Birth            integer,
    SexTypeName      character varying(255),
    Regname          character varying(255),
    AreaName         character varying(255),
    TerName          character varying(255),
    RegTypeName      character varying(255),
    TerTypeName      character varying(255),
    ClassProfileName character varying(255),
    ClassLangName    character varying(255),
    EOName           character varying(255),
    EOTypeName       character varying(255),
    EORegName        character varying(255),
    EOAreaName       character varying(255),
    EOTerName        character varying(255),
    EOParent         character varying(255)
);

CREATE TABLE TestInfo
(
    OUTID      character varying(255),
    Subj       character varying(255),
    TestName   character varying(255),
    TestStatus character varying(255),
    PTName     character varying(255),
    PTRegName  character varying(255),
    PTAreaName character varying(255),
    PTTerName  character varying(255),
    Ball100    numeric,
    Ball12     numeric,
    Ball       numeric,
    DPALevel   character varying(255) DEFAULT NULL,
    AdaptScale integer DEFAULT NULL,
    PRIMARY KEY (OUTID, Subj),
    CONSTRAINT fk_student
        FOREIGN KEY (OUTID)
            REFERENCES PersonInfo (OUTID)
);