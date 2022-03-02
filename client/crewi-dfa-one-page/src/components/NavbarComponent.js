import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Dropdown from 'react-bootstrap/Dropdown'
import { Button, InputRightElementn } from '@chakra-ui/react'

export default class NavbarComponent extends Component {

    render() {
        return(
                <Container>
                    <Navbar expand="lg" variant="light" bg="light">
                            <Nav className="ml-auto">
                            <Navbar.Collapse id="basic-navbar-nav">
                            <Navbar.Brand href="#">Home</Navbar.Brand>
                            <Navbar.Brand href="#">About</Navbar.Brand>
                            <Navbar.Brand href="#">Profile</Navbar.Brand>
                            </Navbar.Collapse>
                            </Nav>
                    </Navbar>
                </Container>
            // <Navbar bg="light" expand="lg">
            //     <Container>
            //         <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
            //         <Navbar.Toggle aria-controls="basic-navbar-nav" />
            //         <Navbar.Collapse id="basic-navbar-nav">
            //             <Nav className="me-auto">
            //                 <Nav.Link href="#home">Home</Nav.Link>
            //                 <Nav.Link href="#link">Link</Nav.Link>
            //                 <NavDropdown title="Dropdown" id="basic-nav-dropdown">
            //                     <NavDropdown.Item href="#">Action</NavDropdown.Item>
            //                     <NavDropdown.Item href="#">Another action</NavDropdown.Item>
            //                     <NavDropdown.Item href="#">Something</NavDropdown.Item>
            //                     <NavDropdown.Divider />
            //                     <NavDropdown.Item href="">Separated link</NavDropdown.Item>
            //                 </NavDropdown>
            //             </Nav>
            //         </Navbar.Collapse>
            //     </Container>
            // </Navbar>
        )
    }

}