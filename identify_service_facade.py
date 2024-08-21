# This class, IdentityServiceFacade, abstracts the interface to external identity service(s) which
# are able to identify "named resources" in input requests (such as a person's name), to a corresponding
# system identifier that can be used for SQL queries (or as an element of an API request for other use cases)


#####################################################
# Mock-up of identifier database with a small set of id records
# These values, along with other fields if required and metadata, are stored in a DBMS in a typical implementation


IDENTITY_DATABASE = {
    'usain bolt': {"id": 13029, "role": 32},  # athlete role
    'isabelle werth': {"id": 129726, "role": 32},  # athlete role
    'nedo nadi': {"id": 84026, "role": 32},  # athlete role
    'allyson felix': {"id": 34551, "role": 32},  # athlete role
    'seb coe': {"id": 78321, "role": 16},  # administrator role
}


class IdentityServiceFacade:

    # A method to resolve a given a set of named resources into identifiers,
    # that can be used in subsequent database queries
    @staticmethod
    def resolve(named_resources: set):
        identifiers = []
        for named_resource in named_resources:
            eid = IDENTITY_DATABASE[named_resource]
            eid['name'] = named_resource
            identifiers.append(eid)
        return identifiers

    # A method to can determine if the given string is a named resourced recognized by the identity service
    # Note: a fuller implementation of this would include the target system/namespace for the identifier
    @staticmethod
    def is_named_resource(named_resource: str) -> bool:
        if named_resource in IDENTITY_DATABASE.keys():
            return True
        else:
            return False
