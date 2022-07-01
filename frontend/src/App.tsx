import React, { useState } from 'react';
import { Button, AppBar, Container, Toolbar } from '@mui/material';
import logo from './logo.svg';
import './App.css';
import Header from './components/header';
import LoginPage from './pages/LoginPage';
import AlertsPage from './pages/AlertsPage';

function App() {

  const [isSignedIn, setIsSignedIn] = useState(false);
  const [user, setUser] = useState(null);
  
  return (
    <div className="App">
    <Header title='BearWatch' subtitle='A subtitle' user='TestUser'/>
    <Button onClick={() => {setIsSignedIn(!isSignedIn)}}>Toggle</Button>
    {!isSignedIn && <LoginPage />}
    {isSignedIn && <AlertsPage />}
    </div>
  );
}

export default App;
