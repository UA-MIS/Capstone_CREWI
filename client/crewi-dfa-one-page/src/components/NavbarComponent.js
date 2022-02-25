import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'

export default class NavbarComponent extends Component {

    render() {
        return(
            <footer>
                <Container>
                    <Navbar expand="lg" variant="light" bg="light">
                        <Container>
                            <Navbar.Brand href="#">Home</Navbar.Brand>
                            <Navbar.Brand href="#">About</Navbar.Brand>
                            <Navbar.Brand href="#">Menu</Navbar.Brand>
                            <Navbar.Brand href="#">Profile</Navbar.Brand>
                            <Navbar.Brand href="#">Menu</Navbar.Brand>
                        </Container>
                    </Navbar>
                </Container>
            </footer>
        )
    }

}