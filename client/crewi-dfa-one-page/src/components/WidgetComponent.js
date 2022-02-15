import React, { Component } from 'react';

//domElement.getAttribute is how you load in custom attributes (this.props works for now)

//this is the main widget component; eventually, we may try to package this up in its own react app and embed it in instead (refer to the Reddit widget stuff for details on that)
export default class WidgetComponent extends Component {

    //this is the child state of the widget; my understanding is that only children of this one could access it
    state = {
        counter: 0,
        time: ""
    }

    //our first attempt at loading in time; it works, but we should probably reformat the time a little
    loadCurrentTime = () => {
        // get a new date (locale machine date time)
        var date = new Date();
        // get the time as a string
        var localTime = date.toLocaleTimeString();

        return date + " " + localTime;
    }

    //for now, just always use arrow functions for click behaviors
    //when the counter is clicked, increment the counter by one and load the time
    counterClick = () => {
        this.setState(state => ({
            counter: state.counter + 1,
            time: this.loadCurrentTime()
        }))
    }

    render() {
        return(
            // this is where the HTML for the widget should be written
            <div>
                <hr></hr>
                <span>Username: </span>
                <span>{this.props.username}</span>
                <br></br>
                <hr></hr>
                {/* this will show the username of the main component; props can be used to grab parent state info */}
                {/* since the parent changing would mean the child is re-rendered, this is updated dynamically (useEffect and some of the hooks work a little differently, refer to the Reddit widget stuff for details) */}
                {/* the same dynamic stuff is true for time */}
                <span>Time: {this.state.time}</span>
                {/* when this button is clicked, it'll call the function that increments counter but also updates time */}
                <button onClick={this.counterClick}>Click To Display Time</button>
            </div>
        )
    }
}