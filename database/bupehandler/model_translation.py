standardOutput = {"name1": None, "name2": None, "name3": None, 
                "website1": None, "website2": None, "telehealth": None, 
                "phone1": None, "phone2": None, "phone3": None, 
                "street1": None, "street2": None, "city": None,
                "state_usa": None, "zipcode": None, 
                "table_url_source": None, ## What is this?
                "latitude": None, "longitude": None
                } 
              ## No translation needed = "bu": None, "bui": None, "bwn": None, "bwon": None, "beri" : None, "bsdm": None, "bum" : None, "bmw": None, "db_field": None, "mu": None, "meth": None, "mm": None, "mmw": None, "dm": None, "nu": None, "nxn": None, "vti": None, "vtrl": None, "rpn": None, 
              ## Removed from specs (July 2021) = "buu": None, "vtm": None, "mdi" [mui]: None, 
mappings = {
    "siterecs_samhsa_ftloc": {
        "website": "website1", 
        "tele": "telehealth", 
        "phone": "phone1", 
        "intake1" : "phone2", 
        "intake2" : "phone3", 
        "zip5": "zipcode"
        },
    "sites_all": dict(),
    "siterecs_samhsa_otp": {
        "program_name": "name1", 
        "dba": "name2", 
        "phone": "phone1", 
        "street" : "street1" 
        },
    "siterecs_dbhids_tad": {
        "phone": "phone1",   ## Since July refresh this data has phone1, phone2
        },
    "siterecs_hfp_fqhc": {
        "name_system": "name1",
        "name_site": "name2",
        "name_short": "name3",
        "website": "website1"
        },
    "siterecs_other_srcs": dict(),
}

class Sites_general_display: 
    def __init__(self, table_name, source_object): 
        self.table_name = table_name
        self.output = standardOutput.copy()
        if self.table_name == "siterecs_samhsa_ftloc": 
            mapping = mappings["siterecs_samhsa_ftloc"]
        elif self.table_name == "sites_all": 
            mapping = mappings["sites_all"]
            # siterecs_samhsa_ftloc_links = ["siterecs_samhsa_ftloc/oid=" + str(x.oid) for x in source_object["id_samhsa_ftloc"]]
            # siterecs_samhsa_otp_links = ["siterecs_samhsa_otp/oid=" + str(x.oid) for x in source_object["id_samhsa_otp"]]
            # siterecs_dbhids_tad_links = ["siterecs_dbhids_tad/oid=" + str(x.oid) for x in source_object["id_dbhids_tad"]]
            # siterecs_hfp_fqhc_links = ["siterecs_hfp_fqhc/oid=" + str(x.oid) for x in source_object["id_hfp_fqhc"]]
            siterecs_samhsa_ftloc_links = ["siterecs_samhsa_ftloc/oid=" + str(source_object["oid"])]
            siterecs_samhsa_otp_links = ["siterecs_samhsa_otp/oid=" + str(source_object["oid"])]
            siterecs_dbhids_tad_links = ["siterecs_dbhids_tad/oid=" + str(source_object["oid"])]
            siterecs_hfp_fqhc_links = ["siterecs_hfp_fqhc/oid=" + str(source_object["oid"])]
            self.output["table_url_source"] = {"siterecs_samhsa_ftloc": siterecs_samhsa_ftloc_links,
            "siterecs_samhsa_otp": siterecs_samhsa_otp_links,
            "siterecs_dbhids_tad": siterecs_dbhids_tad_links,
            "siterecs_hfp_fqhc": siterecs_hfp_fqhc_links}
        elif self.table_name == "siterecs_samhsa_otp": 
            mapping = mappings["siterecs_samhsa_otp"]
        elif self.table_name == "siterecs_dbhids_tad": 
            mapping = mappings["siterecs_dbhids_tad"]
        elif self.table_name == "siterecs_hfp_fqhc": 
            mapping = mappings["siterecs_hfp_fqhc"]
        elif self.table_name == "siterecs_other_srcs": 
            mapping = mappings["siterecs_other_srcs"]
        for key in source_object: 
            if key in self.output: 
                self.output[key] = source_object[key] 
            elif key in mapping: 
                self.output[mapping[key]] = source_object[key] 

def filterKeyToLocalKey(key, table_name):
    try:
        mapping = mappings[table_name]
        if key in mapping.values():
            i = tuple(mapping.values()).index(key)
            localKey = tuple(mapping.keys())[i]
            return localKey
        else:
            return key

    except:
        return key


