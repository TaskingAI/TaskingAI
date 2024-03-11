import { useEffect,ReactNode } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { findRouteByPath } from '../utils/index';
import { router_item } from '../router';
import { verifyToken } from '../axios';
interface AuthRouterProps {
  children: ReactNode;
}
function AuthRouter({ children }: AuthRouterProps) {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const token = localStorage.getItem('token');
  useEffect(() => {
    const checkTokenAndNavigate = async () => {

      if (token) {
        try {
          const res = await verifyToken();
          if (String(res.status) === 'success') {
            if (pathname === '/' || pathname === '/auth/signin' || pathname === 'auth/signup' || pathname === '/auth/reset-password' || pathname === '/auth') {
              navigate('/project');
            }
          } else {
            localStorage.removeItem('token');
            navigate('/auth/signin');
          }
        } catch (err) {
          console.log(err)
          localStorage.removeItem('token');

        }
      } else {
        navigate('/auth/signin');
      }
    };
    checkTokenAndNavigate();


  }, [pathname, token, navigate]);
  const router = findRouteByPath(pathname, router_item);
  if (!router) {
    return <Navigate to="/404" />;
  }

  if (router.meta?.unwantedAuth) {
    return children;
  }
  if (!token) {
    return <Navigate to='/auth/signin' />
  } else {
    return <>{children}</>;
  }
}

export default AuthRouter;
