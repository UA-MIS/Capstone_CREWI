import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'

export default class Navbar extends Component {

    render() {
        return(
            <footer>
                <Container>
                    <Navbar expand="lg" variant="light" bg="light">
                        <Container>
                            <Navbar.Brand href="#">Footer</Navbar.Brand>
                        </Container>
                    </Navbar>
                </Container>
            </footer>
        )
    }

}