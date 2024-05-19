import ProtectedRoute from 'components/AuthRequired';
import FullProfile from 'components/FullProfile';
import DashboardLayout from 'layouts/dashboard';
import ChangePassword from 'pages/ChangePassword';
import Home from 'pages/Home';
import ResetPassword from 'pages/ResetPassword';
import SendResetLink from 'pages/SendResetLink';
import SignIn from 'pages/SignIn';
import SignUp from 'pages/SignUp';
import UpdateProfile from 'pages/UpdateProfile';
import { lazy, Suspense } from 'react';
import { Navigate, Outlet, useRoutes } from 'react-router-dom';

export const IndexPage = lazy(() => import('pages/app'));
export const BlogPage = lazy(() => import('pages/blog'));
export const UserPage = lazy(() => import('pages/user'));
export const LoginPage = lazy(() => import('pages/login'));
export const ProductsPage = lazy(() => import('pages/products'));
export const Page404 = lazy(() => import('pages/page-not-found'));

// ----------------------------------------------------------------------

export default function Router() {
  const routes = useRoutes([
    {
      element: (
        <DashboardLayout>
          <Suspense>
            <Outlet />
          </Suspense>
        </DashboardLayout>
      ),
      children: [
        { path: 'dashboard', element: <IndexPage /> },
        { path: 'user', element: <UserPage /> },
        { path: 'products', element: <ProductsPage /> },
        { path: 'blog', element: <BlogPage /> },
      ],
    },
    {
      path: '/',
      element: (
        <ProtectedRoute>
          <Home />
        </ProtectedRoute>
      )
    },
    {
      path: 'sign-up',
      element: <SignUp />
    },
    {
      path: 'sign-in',
      element: <SignIn />
    },
    {
      path: 'reset-password',
      element: <ResetPassword />
    },
    {
      path: 'change-password',
      element: <ChangePassword />
    },
    {
      path: 'profile',
      element: <FullProfile />
    },
    {
      path: 'update-profile',
      element: <UpdateProfile />
    },
    {
      path: 'send-reset-link',
      element: <SendResetLink />
    },
    {
      path: '404',
      element: <Page404 />,
    },
    {
      path: '*',
      element: <Navigate to="/404" replace />,
    },
  ]);

  return routes;
}
