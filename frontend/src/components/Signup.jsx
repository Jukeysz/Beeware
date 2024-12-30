import { useState } from "react";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import '../assets/Signup.css';

const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { signup } = useAuth();

    const handleSubmission = async (e) => {
        e.preventDefault();
        try {
            await signup(email, username, password);
            navigate('/');
        } catch (error) {
            setError('Email already exists');
        }
    };

    return (
        <div className="auth-container">
            <h1>Sign up</h1>
            <form onSubmit={handleSubmission} className="form">
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
                
                <button type="submit">Sign up</button>
            </form>
            {error && <p>{error}</p>}
        </div>
    )
}

export default Signup;