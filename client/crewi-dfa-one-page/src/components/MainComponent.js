import React, { Component } from 'react';
import LoginComponent from './LoginComponent';
import Widget from './Widget';

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
                {/* login component is being given the handleUpdate function under the name updateState, which will be referenced in its class */}
                <LoginComponent updateState={this.handleUpdate}/>
                {/* the widget just needs a username input, which is taken straight from this state */}
                {/* <WidgetComponent username={this.state.username}/> */}
                <Widget username={this.state.username}/>
            </div>
        )
    }
}