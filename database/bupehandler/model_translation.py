class sites_general_display(): 
    def __init__(self, table_name, source_object): 
        self.table_name = table_name
        self.output = {"name1": None, "name2": None, "name3": None, "website1": None, 
        "website2": None, "telehealth": None, "phone1": None, "phone2": None, 
        "phone3": None, "street1": None, "street2": None, "city": None,
         "state_usa": None, "zipcode": None, "bu": None, "bui": None, 
         "bwn": None, "bwon": None, "beri" : None, "bsdm": None, "bum" : None, 
         "buu": None, "bmw": None, "db_field": None, "mu": None, "meth": None, 
         "mdi" : None, "mm": None, "mmw": None, "dm": None, "nu": None, 
         "nxn": None, "vti": None, "vtm": None, "vtrl": None, "rpn": None}
        if self.table_name == "siterecs_samhsa_ftloc": 
            mapping = {"website": "website1", 
            "tele": "telehealth", 
            "phone": "phone1", 
            "intake1" : "phone2", 
            "intake2" : "phone3", 
            }
            for key in source_object: 
                if key in self.output: 
                    self.output[key] = source_object[key] 
                elif key in mapping: 
                    self.output[mapping[key]] = source_object[key] 




