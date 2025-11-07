def retrieve_object(id,db_model,fail_function,fail_message=None):
    obj = db_model.objects.filter(id=id).first()
    if not obj:
        if not fail_message:
            fail_message = "Invalid Id"
        fail_function(fail_message)
    return obj



def retrieve_query_parameter(request,parameter,fail_function,fail_message=None):
    parameter = request.query_params.get(parameter)
    if not parameter:
        if not fail_message:
            fail_message = "A query parameter is required for this request"
        fail_function(fail_message)
    return parameter
