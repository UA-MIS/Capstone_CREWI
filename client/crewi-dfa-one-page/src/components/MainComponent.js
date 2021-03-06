import React, { Component } from 'react';
import HeaderComponent from './HeaderComponent';
import NavbarComponent from './NavbarComponent';
import FooterComponent from './FooterComponent';
import LoginComponent from './LoginComponent';
import { Grid, Box, Container } from '@chakra-ui/react'
import WidgetIntegrated from './WidgetIntegrated';
import WidgetEmbedded from './WidgetEmbedded';

//this class is our main parent component for the one-page
export default class MainComponent extends Component {

    //top-level state; we can put more stuff in here as needed
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
                <hr/>
                <NavbarComponent/>
                <hr/>
                <br/>
                {/* login component is being given the handleUpdate function under the name updateState, which will be referenced in its class */}
                {/* The grid contains the login component and the widget compnent. Each are called inside the box */}
                <Grid templateColumns='repeat(2,1fr)' gap={0} paddingTop='100px' paddingBottom='100px'>
                <Container className='App-login p-3 mb-5 bg-white' minHeight='300px' maxWidth="500px" borderStyle='solid'>
                    <Box paddingTop='0%'>
                        {/* we use a non-unique ID here, so be careful about making multiple login components */}
                        {/* this will call the updateParent method onChange, which is just whenever the input value changes */}
                        <LoginComponent updateState={this.handleUpdate}/>
                    </Box>
                </Container>
                <Container>
                {/* <Container className='App-login shadow-lg p-3 mb-5 bg-white rounded' minHeight='300px' maxWidth="500" borderStyle="solid">
                    <Box paddingTop='30'> */}
                        {/* the widget just needs a username input, which is taken straight from this state */}
                        <Box>
                            {/* "Embedded" means the widget is being embedded from the crewi-widget React app; use this for testing actual embedding of the widget */}
                            <WidgetEmbedded username={this.state.username} orderLink="https://www.chipotle.com/" failMessage="Our system is unavailable right now. We recommend a Dude-fil-A sandwich!"/>
                            {/* "Integrated" means the widget is just another component; this is fine for development, but is dissimilar to actual use */}
                            {/* <WidgetIntegrated username={this.state.username} orderLink="https://www.chipotle.com/" failMessage="Our system is unavailable right now. We recommend a Dude-fil-A sandwich!"/> */}
                        </Box>
                    {/* </Box>
                </Container> */}
                </Container>
                </Grid>
                <hr/>
                <br/>
                <FooterComponent/>
            </div>
        )
    }
}
