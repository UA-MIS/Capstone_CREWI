import React, { Component } from 'react';
import { Input, InputGroup, InputRightElement, Avatar } from '@chakra-ui/react'

//this will be our login component; it sends the username to the widget when submit is clicked

export default class LoginComponent extends Component {
    render() {
        return(  
            <div>
                <div style = {{paddingBottom: 20}}>
                    <Avatar size='lg'/>
                </div>
                <InputGroup size='md'>
                    <Input
                        id="login" 
                        isInvalid
                        errorBorderColor='black'
                        placeholder='Username'
                        size='md'
                    />
                    <InputRightElement width='4.5rem'>

                    </InputRightElement>
                </InputGroup>
                <br/>
                <InputGroup size='md'>
                    <Input
                        type='password'
                        isInvalid
                        errorBorderColor='black'
                        placeholder='Password'
                        size='md'
                    />
                </InputGroup>
                <br/>
                <button className='widgetButton' id="orderSpan" onClick={this.updateParent}>
                        Login
                        </button>
            </div>
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