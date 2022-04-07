import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import { IconButton } from '@chakra-ui/react'
import { BsCart3 } from 'react-icons/bs';

// navbar at the top of the one-page
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
                        <div style = {{marginLeft: `80%`}}>
                            <IconButton
                            colorScheme='blue'
                            aria-label='Search database'
                            icon={<BsCart3 />}
                            />
                        </div>
        
                </Navbar>
            </Container>
        )
    }

}