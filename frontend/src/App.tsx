import React, { useEffect, useState } from 'react';
import './App.css';
import Header from './components/header';
import LoginPage from './pages/LoginPage';
import AlertsPage from './pages/AlertsPage';
import { User, Token } from './types/models';
import UserService from './services/user.service';

function App() {

  const [token, setToken] = useState<Token | null>(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function fetchUser(token_checked:Token) {
      const user = await UserService.me(token_checked);
      user.token = token_checked;
      setUser(user);
    }
    if (token !== null) {
      fetchUser(token);
    }
  },[token])


  return (
    <div className="App">
    <Header title='BearWatch' subtitle='A subtitle' user='TestUser'/>
    {user === null && <LoginPage handleAuth={setToken}/>}
    {user !== null && <AlertsPage user={user}/>}
    </div>
  );
}

export default App;
