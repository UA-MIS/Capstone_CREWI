import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faYoutube, faFacebook, faTwitter, faInstagram } from "@fortawesome/free-brands-svg-icons";

export default class Header extends Component {

    render() {
        return(
            <div className="social-container" >
                <Navbar.Brand href="#">Contact us</Navbar.Brand>
                <Navbar.Brand>|</Navbar.Brand>
                <Navbar.Brand href="#">Nutrition & Allergens</Navbar.Brand>
                <Navbar.Brand>|</Navbar.Brand>
                <Navbar.Brand href="#">Careers</Navbar.Brand>

                <div style = {{paddingTop: 15}}>
                    <a href="https://www.coolmathgames.com/0-papas-pizzeria"
                        className="youtube social">
                        <FontAwesomeIcon icon={faYoutube} size="2x" />
                    </a>
                    <a href="https://www.coolmathgames.com/0-papas-pizzeria"
                        className="facebook social">
                        <FontAwesomeIcon icon={faFacebook} size="2x" />
                    </a>
                    <a href="https://www.coolmathgames.com/0-papas-pizzeria" className="twitter social">
                        <FontAwesomeIcon icon={faTwitter} size="2x" />
                    </a>
                    <a href="https://www.coolmathgames.com/0-papas-pizzeria"
                        className="instagram social">
                        <FontAwesomeIcon icon={faInstagram} size="2x" />
                    </a>
                </div>
            </div>
        )
    }

}