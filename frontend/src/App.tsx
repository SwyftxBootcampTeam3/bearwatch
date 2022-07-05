import React, { useState } from 'react';
import { Button, AppBar, Container, Toolbar } from '@mui/material';
import logo from './logo.svg';
import './App.css';
import Header from './components/header';
import LoginPage from './pages/LoginPage';
import AlertsPage from './pages/AlertsPage';

function App() {

  const [isSignedIn, setIsSignedIn] = useState(false);
  
  const splashLogo = {
    position: 'absolute' as 'absolute',
    bottom: '0%',
    right: '0%',
    width: '30%',
    zIndex: -1
  }
  const toggleLogin = () => {
    setIsSignedIn(!isSignedIn);
  }
  return (
    <div className="App">
      
    <Header title='BearWatch' subtitle='A subtitle' user='TestUser'/>
    {!isSignedIn && <LoginPage toggleLogin={toggleLogin} />}
    {isSignedIn && <AlertsPage />}
    <img src="/bearwatch-2.png" style={splashLogo}/>
    </div>
  );
}

export default App;
