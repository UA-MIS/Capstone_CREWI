import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Grid, GridItem, Box, Container } from '@chakra-ui/react'

//this will be our login component; it needs to let the user enter a username and password (not a priority at the moment),
//validate the user (will do later), and send the username to the widget (which is what we're looking at now)

// const LoginComponent = () => {
//     return(
//         <Box>
//             {/* we use a non-unique ID here, so be careful about making multiple login components */}
//             {/* this will call the updateParent method onChange, which is just whenever the input value changes */}
//             <input id="login" type="text"></input>
//             <Button onClick={updateParent}>Login</Button>
//         </Box>
//     )
// }

// const updateParent = () => {
//     //grabbing the new username from the input; this is just vanilla JS
//     const newUsername = document.getElementById("login").value;
//     //this.props.updateState is referring to the function that login component was given when made in the main component
//     //updateState is actually the main component's handleUpdate method; in effect, the line below is calling
//     //the main component's handleUpdate function with the new username from the input
//     //this function has access to and changes the main component's state; that's how the child component alters its parent's state
//     //also, since the parent state changing causes it to re-render all its children, the widget (and this component) will be dynamically
//     //updated as changes occur
//     this.props.updateState(newUsername);
// }

// export default LoginComponent

export default class LoginComponent extends Component {
    // loginClick = () => {
    //     this.setState(state => ({
    //         //counter: state.counter + 1,
    //         time: this.updateParent()
    //     }))
    // }

    render() {
        return(  
            <Grid templateColumns='repeat(2,1fr)' gap={100} paddingTop='250px' paddingLeft='200px'> 
                <Container minHeight='300px' maxWidth="500px" borderStyle="solid">
                    <Box paddingTop='100px'>
                        {/* we use a non-unique ID here, so be careful about making multiple login components */}
                        {/* this will call the updateParent method onChange, which is just whenever the input value changes */}
                        <input id="login" type="text"></input>
                        <Button onClick={this.updateParent}>Login</Button>
                    </Box>
                </Container>
                <Container minHeight='300px' maxWidth="500px" borderStyle="solid">
                    <Box paddingTop='100px'>
                        
                    </Box>
                </Container>
            </Grid>
        )
    }

    //this runs whenever the input value is changed
    updateParent = () => {
        //grabbing the new username from the input; this is just vanilla JS
        const newUsername = document.getElementById("login").value;
        //this.props.updateState is referring to the function that login component was given when made in the main component
        //updateState is actually the main component's handleUpdate method; in effect, the line below is calling
        //the main component's handleUpdate function with the new username from the input
        //this function has access to and changes the main component's state; that's how the child component alters its parent's state
        //also, since the parent state changing causes it to re-render all its children, the widget (and this component) will be dynamically
        //updated as changes occur
        this.props.updateState(newUsername);
    }
}