#!/usr/bin/python3

### Static Class
class Table:
    NAMES = ["HDD", "SSD", "CPU", "GPU"] # AKA. data types/categories
    SCHEMAS = {
        "HDD":
            "Time DATETIME\
            , Retailer varchar(255)\
            , Title varchar(255)\
            , URL varchar(255)\
            , PriceAUD int\
            , Brand varchar(255)\
            , Series varchar(255)\
            , ModelNumber varchar(255)\
            , HDDCapacity int\
            , HDDPricePerTB int"
        , "SSD":
            "Time DATETIME\
            , Retailer varchar(255)\
            , Title varchar(255)\
            , URL varchar(255)\
            , PriceAUD int\
            , Brand varchar(255)\
            , Series varchar(255)\
            , ModelNumber varchar(255)\
            , SSDCapacity int\
            , SSDPricePerTB int"
        , "CPU": # TODO: Add unique CPU attributes
            "Time DATETIME\
            , Retailer varchar(255)\
            , Title varchar(255)\
            , URL varchar(255)\
            , PriceAUD int\
            , Brand varchar(255)\
            , Series varchar(255)\
            , ModelNumber varchar(255)"
        , "GPU": # TODO: Add unique GPU attributes
            "Time DATETIME\
            , Retailer varchar(255)\
            , Title varchar(255)\
            , URL varchar(255)\
            , PriceAUD int\
            , Brand varchar(255)\
            , Series varchar(255)\
            , ModelNumber varchar(255)"
    }