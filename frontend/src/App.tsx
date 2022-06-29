import React, { useState } from 'react';
import { Button, AppBar, Container, Toolbar } from '@mui/material';
import logo from './logo.svg';
import './App.css';
import Header from './components/header';
import LoginPage from './pages/LoginPage';

function App() {

  const [isSignedIn, setIsSignedIn] = useState(false);
  return (
    <div className="App">
    <Header title='BearWatch' subtitle='A subtitle' user='TestUser'/>
    {!isSignedIn && <LoginPage />}
    </div>
  );
}

export default App;
