class Tool:

    action_id = "bFBdRJNxmWsSxjmPkN7Xg79y"
    action = None
    action_list = ['object', 'action_id', "operation_id", 'name', 'description', "url", "method", "path_param_schema",
                   "query_param_schema", "body_param_schema", "body_type", "function_def", 'authentication',
                   'openapi_schema', 'created_timestamp', 'updated_timestamp']
    action_keys = set(action_list)
    action_authentication = ['type', 'secret', 'content', 'encrypted']
    action_authentication_keys = set(action_authentication)
    action_schema = ['openapi', 'info', 'servers', 'paths', 'components', 'security']
    action_schema_keys = set(action_schema)
    need_authenticate_list = ["operation_id", 'name', 'description', "url", "method", "path_param_schema",
                              "query_param_schema", "body_param_schema", "body_type", "function_def"]
    run_actions = []

    bundle_instance_id = "open_weather"
    bundle_instance_name = "open_weather"
    bundle_instance_list = ['object', 'bundle_instance_id', "display_credentials", "bundle_id",  'name', "metadata",
                            "plugins", 'description', 'icon_url', 'created_timestamp', 'updated_timestamp']
    bundle_instance_keys = set(bundle_instance_list)
    bundles = []
    bundle_credentials = None
    run_bundles = []

