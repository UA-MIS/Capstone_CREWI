import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'
// import Logo from './Logo.jpg'

// one-page header
export default class Header extends Component {

    render() {
        return(
            <div style={{paddingTop: `20px`, paddingBottom: `20px`}} className="App-header">
                <img src="https://crewi-dfa-one-page.herokuapp.com/dfaLogo.png"/>
                <p></p>
            </div>
           
        )
    }

}