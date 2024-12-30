import { Routes, Route, Link, BrowserRouter } from 'react-router-dom';
import './App.css';

import PrivateRoute from './components/PrivateRoute';
import Main from './components/Main';
import Login from './components/Login';
import Signup from './components/Signup';
import { AuthProvider } from './components/AuthContext';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <nav className='navs'>
          <h1 id='titles'>Game Reviews</h1>
          <div className="headers">
            <Link to="/">home</Link>
            <Link to="/login">sign in</Link>
            <Link to="/signup">sign up</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<PrivateRoute />}>
            <Route path="/" element={<Main />} />
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
