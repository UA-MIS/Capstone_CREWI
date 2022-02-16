import React, { Component } from 'react';

//domElement.getAttribute is how you load in custom attributes (this.props works for now)

//this is the main widget component; eventually, we may try to package this up in its own react app and embed it in instead (refer to the Reddit widget stuff for details on that)
export default class WidgetComponent extends Component {

    //this is the child state of the widget; my understanding is that only children of this one could access it
    // state = {
    //     counter: 0,
    //     time: ""
    // }

    //our first attempt at loading in time; it works, but we should probably reformat the time a little
    loadCurrentTime = () => {
        // get a new date (locale machine date time)
        // var date = new Date();
        // // get the time as a string
        // var localTime = date.toLocaleTimeString();

        // return date + " " + localTime;
        Number.prototype.padLeft = function(base,chr){
            var  len = (String(base || 10).length - String(this).length)+1;
            return len > 0? new Array(len).join(chr || '0')+this : this;
        }
        //returns the date in YYYY-MM-DD HH:MM:SS format
        var d = new Date(),
        dformat = [d.getFullYear(),
                (d.getMonth()+1).padLeft(),
               d.getDate().padLeft()].join('-') +' ' +
              [d.getHours().padLeft(),
               d.getMinutes().padLeft(),
               d.getSeconds().padLeft()].join(':');
        return dformat;
    }

    //for now, just always use arrow functions for click behaviors
    //when the counter is clicked, increment the counter by one and load the time
    // counterClick = () => {
    //         this.setState(state => ({
    //             counter: state.counter + 1,
    //             time: this.loadCurrentTime()
    //         }))
    // }

    render() {
        var time = "";
        try{
            if(this.props.username !== "")
        {
            throw 'No Time';
            time = this.loadCurrentTime();
        } 
        }
        catch{
            time = "Error";
            if(time !== this.loadCurrentTime)
                return(
                <div>
                <hr></hr>
                <span>Username: </span>
                <span>{this.props.username}</span>
                <br></br>
                <hr></hr>
              
                {/* this will show the username of the main component; props can be used to grab parent state info */}
                {/* since the parent changing would mean the child is re-rendered, this is updated dynamically (useEffect and some of the hooks work a little differently, refer to the Reddit widget stuff for details) */}
                {/* the same dynamic stuff is true for time */}
                <span>Time: {time}</span>
                {/* when this button is clicked, it'll call the function that increments counter but also updates time */}
                {/* <button onClick={this.displayClick}>Click Me (Clicked {this.state.counter} times)</button> */}
                <br/>
                <hr/>
                <span>We couldn't load your current time please select an option below:</span>
                <br/>
                <input type="radio" value="Morning" name="dayPart" /> Morning
                <input type="radio" value="Noon" name="dayPart" /> Noon
                <input type="radio" value="Afternoon" name="dayPart" /> Afternoon
                </div>
                )
            }
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
                <span>Time: {time}</span>
                {/* when this button is clicked, it'll call the function that increments counter but also updates time */}
                {/* <button onClick={this.displayClick}>Click Me (Clicked {this.state.counter} times)</button> */}

            </div>
        )
    }
}
    