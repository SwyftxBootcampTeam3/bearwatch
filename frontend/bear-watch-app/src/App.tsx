import React from 'react';
import { Button, AppBar, Container, Toolbar } from '@mui/material';
import logo from './logo.svg';
import './App.css';
import Header from './components/header';

function App() {
  return (
    <div className="App">
    <Header title='BearWatch' subtitle='A subtitle' user='TestUser'/>
    
    </div>
  );
}

export default App;
