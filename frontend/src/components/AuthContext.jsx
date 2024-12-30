import React, { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// For the authentication section, both Copilot and Claude were particulaly great teachers
//because I could learn how to deal with protected components, which is was kind of new to me,
//as I only knew basic React and the standard hooks such as useState and useEffect.

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // I have to make sure that the page does not render immediately, otherwise
    // I would be redirected to login page even if I am already logged in.
    const login = async (email, password) => {
        try {
            const response = await fetch('http://localhost:8000/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ username: email, password: password }),
                credentials: 'include',
            });

            if (response.ok) {
                setIsAuthenticated(true);
                navigate('/');
            } else {
                throw new Error('Login failed');
            }
        } catch (error) {
            console.error(error);
            setError(error.message);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const signup = async (email, username, password) => {
        setIsLoading(true);
        console.log({ email, username, password });
        try {
            const response = await fetch('http://localhost:8000/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, username, password }),
            });

            if (response.ok) {
                await login(email, password);
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Signup failed');
            }
        } catch (error) {
            setError(error.message);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, isLoading, setIsLoading, error, login, signup, setIsAuthenticated, setError }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }

    return context;
};