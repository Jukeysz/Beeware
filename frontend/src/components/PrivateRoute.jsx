import { useEffect } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext';

const PrivateRoute = () => {
    const { isAuthenticated, isLoading, setIsLoading, setIsAuthenticated, setError: setAuthError } = useAuth();

    // maybe transfer this to auth context and use it in the 
    // login and signup components
    useEffect(() => {
        setIsLoading(true);
        const checkAuth = async () => {
            try {
                const response = await fetch('http://localhost:8000/auth/verify', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    setIsAuthenticated(false);
                } else {
                    setIsAuthenticated(true);
                }
            } catch (error) {
                setIsAuthenticated(false);
                setAuthError('You are not authenticated');
            } finally {
                setIsLoading(false);
            }
        };

        checkAuth();
    }, [setIsAuthenticated, setAuthError, setIsLoading]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
}

export default PrivateRoute;