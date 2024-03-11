import { request } from '../utils/index';
// import { getSpaceAndProjectIds } from '../utils/util'
export const fetchAssistantRequest = () => {
  return {
    type: 'FETCH_ASSISTANT_REQUEST',
  };
};

export const fetchAssistantSuccess = (users: any) => {
  return {
    type: 'FETCH_ASSISTANT_SUCCESS',
    payload: users,
  };
};

export const fetchRetrievalFailure = (error: any) => {
  return {
    type: 'FETCH_RETRIEVAL_FAILURE',
    payload: error,
  };
};
export const fetchRetrievalRequest = () => {
  return {
    type: 'FETCH_RETRIEVAL_REQUEST',
  };
};

export const fetchRetrievalSuccess = (users: any) => {
  return {
    type: 'FETCH_RETRIEVAL_SUCCESS',
    payload: users,
  };
};

export const fetchAssistantFailure = (error: any) => {
  return {
    type: 'FETCH_ASSISTANT_FAILURE',
    payload: error,
  };
};
export const fetchModelRequest = () => {
  return {
    type: 'FETCH_MODEL_REQUEST',
  };
};

export const fetchModelSuccess = (users: any) => {
  return {
    type: 'FETCH_MODEL_SUCCESS',
    payload: users,
  };
};

export const fetchModelFailure = (error: any) => {
  return {
    type: 'FETCH_MODEL_FAILURE',
    payload: error,
  };
};
export const fetchApikeysRequest = () => {
  return {
    type: 'FETCH_APIKEY_REQUEST',
  };
};

export const fetchApikeysSuccess = (users: any) => {
  return {
    type: 'FETCH_APIKEY_SUCCESS',
    payload: users,
  };
};

export const fetchApikeysFailure = (error: any) => {
  return {
    type: 'FETCH_APIKEY_FAILURE',
    payload: error,
  };
};
export const fetchPluginRequest = () => {
  return {
    type: 'FETCH_PLUGIN_REQUEST',
  };
};

export const fetchPluginSuccess = (users: any) => {
  return {
    type: 'FETCH_PLUGIN_SUCCESS',
    payload: users,
  };
};

export const fetchPluginFailure = (error: any) => {
  return {
    type: 'FETCH_PLUGIN_FAILURE',
    payload: error,
  };
};
export const fetchActionRequest = () => {
  return {
    type: 'FETCH_ACTION_REQUEST',
  };
};

export const fetchActionSuccess = (users: any) => {
  return {
    type: 'FETCH_ACTION_SUCCESS',
    payload: users,
  };
};

export const fetchActionFailure = (error: any) => {
  return {
    type: 'FETCH_ACTION_FAILURE',
    payload: error,
  };
};
export const setLoading = (isLoading: boolean) => {
  return {
    type: 'SET_LOADING',
    payload: isLoading,
  };
};
export const fetchAssistantsData = () => {
  return (dispatch: any) => {
    const project_base_url = 'api/v1'

    dispatch(fetchAssistantRequest());
    request.get(`${project_base_url}/assistants?limit=20`)
      .then(response => {
        dispatch(fetchAssistantSuccess(response));
      })
      .catch(error => {
        dispatch(fetchAssistantFailure(error.message));
      });
  };
};
export const fetchModelsData = (limit: number) => {
  return (dispatch: any) => {
    const project_base_url = 'api/v1'
    dispatch(fetchModelRequest());
    request.get(`${project_base_url}/models?limit=${limit}`)
      .then(response => {
        dispatch(fetchModelSuccess(response));
      })
      .catch(error => {
        dispatch(fetchModelFailure(error.message));
      });
  };
};
export const fetchApikeysData = (limit: number) => {
  return (dispatch: any) => {
    const project_base_url = 'api/v1'
    dispatch(fetchApikeysRequest());
    request.get(`${project_base_url}/apikeys?limit=${limit}`)
      .then(response => {
        dispatch(fetchApikeysSuccess(response));
      })
      .catch(error => {
        dispatch(fetchApikeysFailure(error.message));
      });
  };
};
export const fetchRetrievalData = (limit: number) => {
  return (dispatch: any) => {
    const project_base_url ='api/v1'
    dispatch(fetchRetrievalRequest());
    request.get(`${project_base_url}/collections?limit=${limit}`)
      .then(response => {
        dispatch(fetchRetrievalSuccess(response));
      })
      .catch(error => {
        dispatch(fetchRetrievalFailure(error.message));
      });
  };
};
export const fetchPluginData = (limit: number) => {
  return (dispatch: any) => {
    const project_base_url = 'api/v1'
    dispatch(fetchPluginRequest());
    request.get(`${project_base_url}/bundle_instances?limit=${limit}`)
      .then(response => {
        dispatch(fetchPluginSuccess(response));
      })
      .catch(error => {
        dispatch(fetchPluginFailure(error.message));
      });
  };
};
export const setLoaded = (loaded: any) => {
  return {
    type: 'SET_LOADED',
    payload: loaded,
  };
};
export const fetchActionData = (limit: number) => {
  return (dispatch: any) => {
    const project_base_url = 'api/v1'
    dispatch(fetchActionRequest());
    request.get(`${project_base_url}/actions?limit=${limit}`)
      .then(response => {
        dispatch(fetchActionSuccess(response));
      })
      .catch(error => {
        dispatch(fetchActionFailure(error.message));
      });
  };
};
