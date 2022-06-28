import React from 'react';
import { Navbar, Nav, Container, Button} from 'react-bootstrap';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
     <Navbar bg="dark" variant="dark">
    <Container>
    <Navbar.Brand href="#home">Navbar</Navbar.Brand>
    <Nav className="me-auto">
      <Nav.Link href="#home">Home</Nav.Link>
      <Nav.Link href="#features">Features</Nav.Link>
      <Nav.Link href="#pricing">Pricing</Nav.Link>
    </Nav>
    </Container>
  </Navbar>
  <Button variant="primary">submit</Button>
    </div>
  );
}

export default App;
