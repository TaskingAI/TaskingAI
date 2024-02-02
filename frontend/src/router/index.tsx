import { lazy } from 'react'
import lazyLoad from "./lazyload"
import { Navigate } from 'react-router-dom'
// import Login from '@/views/login/index'

export const router_item = [
    {
        path: '/', key: '/', element: <Navigate to="/auth/signin" />, meta: {
            unwantedAuth: true
        }
    },
    {
        path: '/auth',  element: <Navigate to="/auth/signin" />, key: '/auth', meta: {
            unwantedAuth: true
        }
    },
    {
        path: '/auth/signin',
        element: lazyLoad(lazy(() => import("@/views/login/index.tsx"))),
        key: 'login',
        meta: {
            unwantedAuth: true
        }
    },
    {
        path: '/project',
        element: lazyLoad(lazy(() => import("@/views/projectHome/index.tsx"))),
        key: 'projectHome',
        children: [
            { path: '', element: lazyLoad(lazy(() => import("@/components/modelsPage"))), key: 'project' },
            { path: 'models', element: lazyLoad(lazy(() => import("@/components/modelsPage"))), key: 'models' },
            { path: 'playground', element: lazyLoad(lazy(() => import("@/components/playground/index.tsx"))), key: 'playground' },
            { path: 'assistants', element: lazyLoad(lazy(() => import("@/components/assistants/index.tsx"))), key: 'assistants' },
            {
                path: 'collections/:collectionId?', element: lazyLoad(lazy(() => import("@/components/retrieval/index.tsx"))), key: 'retrieval',
                children: [
                    { path: 'records', element: lazyLoad(lazy(() => import("@/components/recordPage/index.tsx")) as React.ComponentType<object>), key: 'records', },
                    { path: 'chunks', element: lazyLoad(lazy(() => import("@/components/chunkPage/index.tsx")) as React.ComponentType<object>), key: 'chunk', },
                ]
            },
            {
                path: 'tools', element: lazyLoad(lazy(() => import("@/components/plugins/index.tsx"))), key: 'plugins',
                children: [
                    { path: '', element: lazyLoad(lazy(() => import("@/components/actions/index.tsx"))), key: 'actions' },
                    { path: 'actions', element: lazyLoad(lazy(() => import("@/components/actions/index.tsx"))), key: 'actions' },
                ]
            },
            { path: 'apikeys', element: lazyLoad(lazy(() => import("@/components/apiKey/index.tsx"))), key: 'apiKeys' },
           
        ],
    },
    {
        path: '*',
        element: lazyLoad(lazy(() => import("@/views/notFound/index.tsx"))),
        key: 'NotFound',
        meta: {
            unwantedAuth: true
        }
    }
]