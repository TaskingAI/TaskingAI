
const initialAccountState = {
    accountData: null,

};

const AccountReducer = (state = initialAccountState, action: any) => {
    switch (action.type) {
        case 'ACCOUNT_DATA':
            return {
                ...state,
                accountData: action.payload,
            };
        default:
            return state;
    }
};
const initialOrganizationState = {
    organizationData: null,
};

const organizationReducer = (state = initialOrganizationState, action: any) => {
    switch (action.type) {
        case 'ORGANIZATION_DATA':
            return {
                ...state,
                organizationData: action.payload,
            };
        default:
            return state;
    }
};
const initialSubscriptionState = {
    subscriptionData: null,
};
const subscriptionReducer = (state = initialSubscriptionState, action: any) => {
    switch (action.type) {
        case 'SUBSCRIPTION_DATA':
            return {
                ...state,
                subscriptionData: action.payload,
            };
        default:
            return state;
    }
}
const initialInvoiceTopUpState = {
    invoiceTopUpData: null,

}
const invoiceTopUpReducer = (state = initialInvoiceTopUpState, action: any) => {
    switch (action.type) {
        case 'INVOICE_TOPUP_DATA':
            return {
                ...state,
                invoiceTopUpData: action.payload
            };
        default:
            return state;
    }
}
const initialInvoiceSubscriptionState = {
    invoiceSubscriptionData: null,
}
const invoiceSubscriptionReducer = (state = initialInvoiceSubscriptionState, action: any) => {
    switch (action.type) {
        case 'INVOICE_SUBSCRIPTION_DATA':
            return {
                ...state,
                invoiceSubscriptionData: action.payload
            };
        default:
            return state;
    }
}
const initialMemberState = {
    memberData: null,

}
const memberReducer = (state = initialMemberState, action: any) => {
    switch (action.type) {
        case 'MEMBER_DATA':
            return {
                ...state,
                memberData: action.payload
            };
        default:
            return state;
    }

};
const initialEmailState = {
    emailData: '',
}
const emailReducer = (state = initialEmailState, action: any) => {
    switch (action.type) {
        case 'EMAIL_DATA':
            return {
                ...state,
                emailData: action.payload
            };
        default:
            return state;
    }
}
const initialProjectList = {
    projectList: [],
    hasMore:  false
}
const projectReducer = (state = initialProjectList, action: any) => {
    switch (action.type) {
        case 'PROJECT_LIST':
            return {
                ...state,
                projectList: action.payload
            };
        case 'PROJECT_LIST_HAS_MORE':
            return {
                ...state,
                ReduxHasMore: action.payload
            };
        default:
            return state;
    }
}
const initialProjectLoading = {
    loading: false
}
const projectLoadingReducer = (state = initialProjectLoading, action: any) => {
    switch (action.type) {
        case 'PROJECT_LOADING':
            return {
                ...state,
                projectLoading: action.payload
            };
        default:
            return state;
    }
}
const initialPlaygroundType = {
    playgroundType: 'assistant',
}
const playgroundTypeReducer = (state = initialPlaygroundType, action: any) => {
    switch (action.type) {
        case 'PLAYGROUND_TYPE':
            return {
                ...state,
                playgroundType: action.payload
            }
        default:
            return state;
    }
}
const initialAssistantId = {
    assistantPlaygroundId: ''
}
const assistantIdReducer = (state = initialAssistantId, action: any) => {
    switch (action.type) {
        case 'ASSISTANT_ID':
            return {
                ...state,
                assistantPlaygroundId: action.payload
            }
        default:
            return state;
    }
}
const initialModel = {
    modelId: '',
    modelName: ''
}
const modelIdReducer = (state = initialModel, action: any) => {
    switch (action.type) {
        case 'MODEL_ID':
            return {
                ...state,
                modelId: action.payload
            }
        case 'MODEL_NAME':
            return {
                ...state,
                modelName: action.payload
            }
        default:
            return state;
    }
}

export { AccountReducer,emailReducer,invoiceTopUpReducer,memberReducer,invoiceSubscriptionReducer,subscriptionReducer, modelIdReducer , assistantIdReducer, playgroundTypeReducer, organizationReducer, projectReducer, projectLoadingReducer }
