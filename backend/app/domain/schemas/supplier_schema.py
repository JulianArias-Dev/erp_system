def supplierEntity(item) -> dict :
    return {
        "id" : item["id"],
        "name" : item["name"],
        "email" : item["email"],
        "password" : item["password"],
    }
    
def suppliersEntity(entity) -> list : 
    [supplierEntity(item) for item in entity] 