import React, { Component } from 'react';
import HeaderComponent from './HeaderComponent';
import NavbarComponent from './NavbarComponent';
import FooterComponent from './FooterComponent';
import LoginComponent from './LoginComponent';
import Widget from './Widget';
import Button from 'react-bootstrap/Button';
import { Grid, GridItem, Box, Container } from '@chakra-ui/react'

//this class is going to be our main parent component for the one-page
export default class MainComponent extends Component {

    //this is the top-level state; we can put more stuff in here as needed
    state = {
        username: ""
    }

    //whenever this method is called, set the state's username to newUsername
    handleUpdate = (newUsername) => {
        this.setState({
            username: newUsername
        })
    }

    //renders out the login and widget components in parallel; they are siblings, so they have to use this main component as an intermediary to communicate
    render() {
        return(
            <div>
                <HeaderComponent/>
                <NavbarComponent/>
                {/* login component is being given the handleUpdate function under the name updateState, which will be referenced in its class */}

                {/* The grid contains the login component and the widget compnent. Each are called inside the box */}
                <Grid templateColumns='repeat(2,1fr)' gap={0} paddingTop='100px' paddingBottom='100px'>
                <Container className='App-login shadow-lg p-3 mb-5 bg-white rounded' minHeight='300px' maxWidth="500px" borderStyle='solid'>
                    <Box paddingTop='20%'>
                        {/* we use a non-unique ID here, so be careful about making multiple login components */}
                        {/* this will call the updateParent method onChange, which is just whenever the input value changes */}
                        <LoginComponent updateState={this.handleUpdate}/>
                    </Box>
                </Container>
                <Container className='App-login shadow-lg p-3 mb-5 bg-white rounded' minHeight='300px' maxWidth="500" borderStyle="solid">
                    <Box paddingTop='150'>
                        {/* the widget just needs a username input, which is taken straight from this state */}
                        <Widget username={this.state.username}/>
                    </Box>
                </Container>
                </Grid>
                <FooterComponent/>
            </div>
        )
    }
}
