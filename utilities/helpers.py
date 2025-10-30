def retrieve_object(id,db_model,fail_function,fail_message=None):
    obj = db_model.objects.filter(id=id).first()
    if not obj:
        if not fail_message:
            fail_message = "Invalid Id"
        fail_function(fail_message)
    return obj


