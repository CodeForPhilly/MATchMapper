class Sites_general_display: 
    def __init__(self, table_name, source_object): 
        self.table_name = table_name
        self.output = {"name1": None, "name2": None, "name3": None, "website1": None, 
        "website2": None, "telehealth": None, "phone1": None, "phone2": None, 
        "phone3": None, "street1": None, "street2": None, "city": None,
         "state_usa": None, "zipcode": None, "bu": None, "bui": None, 
         "bwn": None, "bwon": None, "beri" : None, "bsdm": None, "bum" : None, 
         "buu": None, "bmw": None, "db_field": None, "mu": None, "meth": None, 
         "mdi" : None, "mm": None, "mmw": None, "dm": None, "nu": None, 
         "nxn": None, "vti": None, "vtm": None, "vtrl": None, "rpn": None, "table_url_source": None}
        if self.table_name == "siterecs_samhsa_ftloc": 
            mapping = {"website": "website1", 
            "tele": "telehealth", 
            "phone": "phone1", 
            "intake1" : "phone2", 
            "intake2" : "phone3", 
            }
        elif self.table_name == "sites_all": 
            mapping = dict()
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
            mapping = {"program_name": "name1", 
            "dba": "name2", 
            "phone": "phone1", 
            "street" : "street1" 
            }
        elif self.table_name == "siterecs_dbhids_tad": 
            mapping = {"phone": "phone1"}
        elif self.table_name == "siterecs_hfp_fqhc": 
            mapping = {"name_system": "name1",
            "name_site": "name2",
            "name_short": "name3",
            "website": "website1"
            }
        elif self.table_name == "siterecs_other_srcs": 
            mapping = dict()
        for key in source_object: 
            if key in self.output: 
                self.output[key] = source_object[key] 
            elif key in mapping: 
                self.output[mapping[key]] = source_object[key] 




