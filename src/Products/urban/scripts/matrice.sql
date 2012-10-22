
CREATE TABLE ART
 (
    daa         Double precision, 
    t05         Double precision, 
    t06         Double precision, 
    t07         Double precision, 
    t01         Double precision, 
    t02         Double precision, 
    t03         Double precision, 
    t04         Double precision, 
    t08         Double precision, 
    t09         Double precision, 
    t10         Double precision, 
    t11         Double precision, 
    t12         Double precision, 
    t13         Double precision, 
    t14         Double precision, 
    da          Bigint
);

CREATE TABLE DA
 (
    da          Bigint, 
    dan1            Character varying (64), 
    lt          Character varying (2), 
    admnr           Character varying (10), 
    da1         Character varying (4), 
    adm1            Character varying (50), 
    mut         Character varying (4), 
    dan2            Character varying (64), 
    adm2            Character varying (50),
    CONSTRAINT da_pk PRIMARY KEY (da)
);

CREATE TABLE LT
 (
    LT          smallint
);

CREATE TABLE MAP
 (
    CapaKey         Character varying (34), 
    UrbainKey           Character varying (42), 
    daa         Double precision, 
    ord         Character varying (8), 
    pe          Character varying (424), 
    adr1            Character varying (60), 
    adr2            Character varying (88), 
    pe2         Character varying (2), 
    sl1         Character varying (74), 
    prc         Character varying (24), 
    na1         Character varying (20), 
    co1         Double precision, 
    cod1            Character varying (4), 
    ri1         Double precision, 
    acj         Character varying (8), 
    tv          Character varying (2), 
    prc2            Character varying (2)
);

CREATE TABLE NA
 (
    na          Character varying (68), 
    naflag          Character varying (2)
);

CREATE TABLE NSR
 (
    admnr           Character varying (10), 
    rscod           real, 
    nsr         Character varying (74), 
    rslt            Character varying (2), 
    rspos           real, 
    nsrprov         Character varying (74)
);

CREATE TABLE PE
 (
    pe          Character varying (424), 
    cod         Character varying (30), 
    daa         Double precision, 
    pos         smallint, 
    adr1            Character varying (60), 
    adr2            Character varying (88), 
    lt          Character varying (4), 
    dr          Character varying (90), 
    dr2         Character varying (6)
);

CREATE TABLE PRC
 (
    daa         Double precision, 
    ord         Character varying (8), 
    "in"            Character varying (4), 
    ante            Character varying (18), 
    sl1         Character varying (74), 
    prc         Character varying (24), 
    na1         Character varying (20), 
    co1         Double precision, 
    ha1         Character varying (16), 
    cod1            Character varying (4), 
    ri1         Double precision, 
    cac         Character varying (8), 
    ddi         Character varying (4), 
    cc          Character varying (76), 
    notif           Character varying (8), 
    caoo            Character varying (420), 
    rscod           real, 
    rslt            Character varying (2), 
    rsnr            real, 
    rspos           real, 
    acj         Character varying (8), 
    n1          Character varying (2), 
    tv          Character varying (2), 
    mo          Character varying (4), 
    ha          Character varying (4), 
    pw1         Character varying (4), 
    sl2         Character varying (70), 
    pw2         Character varying (4), 
    na2         Character varying (20), 
    n2          Character varying (2), 
    co2         Double precision, 
    ha2         Character varying (16), 
    cod2            Character varying (4), 
    ri2         Double precision, 
    sl3         Character varying (70), 
    pw3         Character varying (4), 
    na3         Character varying (20), 
    n3          Character varying (2), 
    co3         Double precision, 
    ha3         Character varying (16), 
    cod3            Character varying (4), 
    ri3         Double precision, 
    pw4         Character varying (4), 
    na4         Character varying (20), 
    n4          Character varying (2), 
    co4         Double precision, 
    ha4         Character varying (16), 
    cod4            Character varying (4), 
    ri4         Double precision, 
    na5         Character varying (20), 
    n5          Character varying (2), 
    co5         Double precision, 
    ha5         Character varying (16), 
    cod5            Character varying (4), 
    ri5         Double precision, 
    na6         Character varying (20), 
    n6          Character varying (2), 
    co6         Double precision, 
    ha6         Character varying (16), 
    cod6            Character varying (4), 
    ri6         Double precision, 
    na7         Character varying (20), 
    n7          Character varying (2), 
    co7         Double precision, 
    ha7         Character varying (16), 
    cod7            Character varying (4), 
    ri7         Double precision, 
    na8         Character varying (20), 
    n8          Character varying (2), 
    co8         Double precision, 
    ha8         Character varying (16), 
    cod8            Character varying (4), 
    ri8         Double precision, 
    na9         Character varying (20), 
    cod9            Character varying (4), 
    ri9         Double precision, 
    na10            Character varying (20), 
    cod10           Character varying (4), 
    ri10            Double precision, 
    na11            Character varying (20), 
    cod11           Character varying (4), 
    ri11            Double precision, 
    n14         Double precision, 
    n56         Double precision, 
    sheet           Character varying (12)
);

CREATE TABLE PAS
 (
    daS         Character varying (12), 
    inA         smallint, 
    artA            Bigint, 
    ordA            Integer, 
    prcA            Character varying (24), 
    inB         smallint, 
    artB            Bigint, 
    ordB            Integer, 
    prcB1           Character varying (22), 
    sl2B            Character varying (20), 
    crscB           Character varying (6), 
    inC         smallint, 
    artC            Bigint, 
    ordC            Integer, 
    prcC            Character varying (24)
);

