import React, { useEffect, useState } from 'react'

// this is the functional code of the widget; this will load the widget as a component rather than grabbing the actual widget from the static files
// this can be useful for quickly testing stuff, but make sure to update the actual widget in crewi-widget
const WidgetIntegrated = (props) => {
    //these happen once no matter what; they will not run again
    const [username, setUsername] = useState("");
    const [orderLink, setOrderLink] = useState("");
    const [failMessage, setFailMessage] = useState("");
    const [status, setStatus] = useState("loading");
    const [timeSlot, setTimeSlot] = useState("");
    const [imgUrl, setImgUrl] = useState("");
    const [itemName, setItemName] = useState("");
    const [closestLocation, setClosestLocation] = useState("");
    const [recentLocation, setRecentLocation] = useState("");
    const [bestLocation, setBestLocation] = useState("");
    const [statusMessage, setStatusMessage] = useState("");

    let time = "";
    let timeStatus = "";

    //this runs the first time, and then again whenever username is changed 
    useEffect(() => {
        timeStatus = "";
        requestRecommendation();
    }, [username])

    // fetches the recommendation, might need to be async? doesn't look like it does at the moment
    const fetchRecommendation = function(username, time, timeSlot, latitude, longitude) {
        // for local testing use this:
        // fetch(`http://localhost:8000/recommendation/`, {
        // for testing the deployed hosting
        fetch(`https://crewi-engine.herokuapp.com/recommendation/`, {
            // GET can't take a request body, apparently
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            // request parameters for getting a recommendation
            body: JSON.stringify({
              username: username,
              time: time,
              timeSlot: timeSlot,
              latitude: latitude,
              longitude: longitude
            })
        })
            .then(response => response.json())
            .then(result => {
                // logs the result, updates the state (which will update the DOM)
                console.log(result);

                // updating item info
                setImgUrl(result.items[0].imgUrl);
                setItemName(result.items[0].name);

                // updating location info
                setClosestLocation(result.locations.closestLocation);
                setRecentLocation(result.locations.recentLocation);
                setBestLocation(result.locations.bestLocation);

                // determining the status message
                determineStatus(result.statuses);

                // going to the success screen
                setStatus("success");
            }).catch(error => {
                // logs the error, updates state to fail; this is the full engine failure, so there won't be a status array
                console.log(error);
                setStatus("fail");
            })
    }

    //our first attempt at loading in time; it works, but we should probably reformat the time a little
    //if this fails, the exception will be caught in requestRec
    const loadCurrentTime = function() {
        // throw 'exception'
        // I'd like to walk through this at some point to make sure edge cases are covered
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

    // gets coordinates then finds the address from there; "location" is the address we need for the request
    const loadCurrentLocation = async function() {
        try {
            // result will be a Geolocation object; await means execution will pause here until finished
            let result = await getCoordinates();   

            // returns the coordinates to requestRecommendation, takes in coordinates and options
            return [result.coords.latitude, result.coords.longitude]
        } catch {
            setStatus("no-location loading");
            return ["BLOCKED", "BLOCKED"];
        }
    }

    // returns current latitude and longitude
    const getCoordinates = async function() {
        // gets the current coordinates using geolocator
        const coordinatePromise = new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        
        // returns coords once the promise is resolved/rejected, which happens when geolocating is complete
        return await coordinatePromise;
    }

    //this runs whenever state or props are updated; it updates token so that the useEffect above will run
    //props are updated when the button is clicked bc it will update the main state, etc.
    useEffect(() => {
        setUsername(props.username);
        setOrderLink(props.orderLink);

        // setting the fail message; using a default if one is not provided
        if (props.failMessage) {
            setFailMessage(props.failMessage);
        } else {
            setFailMessage("Recommendation failed");
        }
    })

    // runs whenever radio buttons are clicked
    const onValueChange = (event) => {
        // updates time slot, re-renders so the buttons will actually be checked
        setTimeSlot(event.target.value);
    }

    // runs when submitting time slot
    const formSubmit = (event) => {
        // prevents redirect on form submit
        event.preventDefault();
        // only proceed if the user actually picks a time slot; otherwise, just ignore the submit until they do
        if (timeSlot != "") {
            timeStatus = "time slot selected";
            // because the requesting useEffect only runs on username change, request has to be called again
            requestRecommendation();
        }
    }

    // contains overarching logic for loading data, requesting recommendation, and updating status accordingly
    const requestRecommendation = async function() {
        // requesting is when the widget is "loading"
        setStatus("loading");

        // reset statuses whenever reloading widget; these should be overwritten anyway
        setStatusMessage("");

        // if time slot is blank, try to request with time loading
        if (timeStatus == "") {
            try {
                // if this fails, no time is invoked
                time = loadCurrentTime();

                try {
                    // grabs location (meaning street address) and waits here so that fetchRec won't get called until this done
                    // loadCurrentLocation needs to return a blank or sentinel value into location if something fails
                    let coordinates = await loadCurrentLocation();
                    const latitude = coordinates[0];
                    const longitude = coordinates[1];

                    // this will actually grab the rec and update the status for the DOM
                    fetchRecommendation(username, time, timeSlot, latitude, longitude);
                
                } catch (error) {
                    console.log(error);
                    // if something goes wrong, go into no-time mode (again, restructure this later)
                    setStatus("fail");
                }
            } catch (error) {
                // if time loading failed, update status and don't continue the request
                console.error(error);
                setTimeSlot("");
                setStatus("no-time");
            }
        } else {
            // this will run if time failed and the user picked a time slot
            try {
                // grabs location (meaning street address) and waits here so that fetchRec won't get called until this done
                // loadCurrentLocation needs to return a blank or sentinel value into location if something fails
                let coordinates = await loadCurrentLocation();
                const latitude = coordinates[0];
                const longitude = coordinates[1];

                // this will actually grab the rec and update the status for the DOM
                fetchRecommendation(username, time, timeSlot, latitude, longitude);
            } catch (error) {
                console.log(error);
                // if something goes wrong, display fail
                setStatus("fail");
            }
        }

        // time slot needs to be reset after each request so that loading time will be re-attempted
        
    }

    const clickOrder = () =>{
        window.location.href = orderLink;
    }

    const copyLocation = location => {
        navigator.clipboard.writeText(location);
    }

    const showBest = () => {
        // Get the snackbar DIV
        var x = document.getElementById("bestSnackbar");

        document.getElementById("bestButton").disabled = true;

        // Add the "show" class to DIV
        x.className += "show";

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){
            x.className = x.className.replace("show", ""); 
            document.getElementById("bestButton").disabled = false;
        }, 3000);
    }

    const showClosest = () => {
        // Get the snackbar DIV
        var x = document.getElementById("closestSnackbar");

        document.getElementById("closestButton").disabled = true;

        // Add the "show" class to DIV
        x.className += "show";

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){
            x.className = x.className.replace("show", ""); 
            document.getElementById("closestButton").disabled = false;
        }, 3000);
    }

    const showRecent = () => {
        // Get the snackbar DIV
        var x = document.getElementById("recentSnackbar");

        document.getElementById("recentButton").disabled = true;

        // Add the "show" class to DIV
        x.className += "show";

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){
            x.className = x.className.replace("show", ""); 
            document.getElementById("recentButton").disabled = false;
        }, 3000);
    }

    const showStatus = () => {
        // Get the snackbar DIV
        var x = document.getElementById("statusSnackbar");

        document.getElementById("statusBtn").disabled = true;

        // Add the "show" class to DIV
        x.className += "show";

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){
            x.className = x.className.replace("show", ""); 
            document.getElementById("statusBtn").disabled = false;
        }, 3000);        
    }

    // this method determines what message to display to the end user based on the engine's issues and fails
    // lots of room for adjustment here, refer to documentation
    const determineStatus = (statusArray) => {
        // msg is defaulted to blank, if there isn't a global fail, bad username, or location fail, it'll stay blank
        // the other fails/issues aren't of top priority, so this keeps the user messages limited
        // the response can still be logged to see all statuses if needed for debugging
        let msg = "";
        
        // global fail takes priority, it means everything failed and the default is being used
        // then bad username (if one was given), then location services being blocked
        // could easily add a scenario for bad username and bad location, but that's probably less useful
        // in theory if both are broken the user will just fix them one at a time
        // plenty of adjustments could be made, can document and revise as needed
        if (statusArray.includes("GLOBAL_FAIL")) {
            msg = "Unable to make a customized recommendation at this time...";
        } else if (statusArray.includes("BAD_USERNAME_ISSUE") && username) {
            msg = "No user found with that username, try signing in again";
        } else if (statusArray.includes("RECOMMEND_CLOSEST_ISSUE")) {
            msg = "We couldn't find you, double check location permissions";
        }

        setStatusMessage(msg);
    }

    // DISPLAY SECTION

    // loading display
    if (status == "loading")
    {
        return(
            <div className='widgetLoading widgetBox boxShadowImitation' style={{
                backgroundImage: `url(https://drive.google.com/uc?export=view&id=1EEZ7JydK3G1W4rXwCtfgZj0HXrBWHbpr)`
            }}>
            </div>        
        )
    }

    else if (status == "no-location loading")
    {
        return(
            <div className='widgetLoading widgetBox boxShadowImitation' style={{
                backgroundImage: `url(https://drive.google.com/uc?export=view&id=1EEZ7JydK3G1W4rXwCtfgZj0HXrBWHbpr)`
            }}>
                <span className='widgetText'>
                    Location unavailable
                </span>
            </div>
        )
    }

    // no-time display

    else if (status == "no-time")
    {
        //I think here we would want to display username if the end user has enetered it
        return(
            <div className='widgetBox boxShadowImitation' style={{
                backgroundImage: `none`}}>
                
                <span>Unable to load time, please select an option below:</span>
                <hr />
                <br />
                <form onSubmit={formSubmit}>
                    <div style={{ paddingLeft: '38%', textAlign: "left"}}>
                            <div className="radio">
                                <label>
                                    <input
                                        type="radio"
                                        value="Morning"
                                        name="dayPart"
                                        checked={timeSlot == "Morning"} 
                                        onChange={onValueChange}
                                    />&nbsp;
                                    Morning
                                </label>
                            </div>
                            <div className="radio">
                                <label>
                                    <input
                                        type="radio"
                                        value="Afternoon" 
                                        name="dayPart"
                                        checked={timeSlot == "Afternoon"} 
                                        onChange={onValueChange}
                                    />&nbsp;
                                    Afternoon
                                </label>
                            </div>
                            <div className="radio">
                                <label>
                                    <input
                                        type="radio"
                                        value="Night"
                                        name="dayPart"
                                        checked={timeSlot == "Night"}
                                        onChange={onValueChange}
                                    />&nbsp;
                                    Night
                                </label>
                            </div>
                        </div>
                            <br/>
                            <button type="submit" className='widgetButton'>Submit</button>
                        </form>                
            </div>
        )
    }

    // success display (if rec is loaded successfully)

    else if (status == "success")
    {
        // location for showing status
        let statusHtml;
        if (statusMessage) {
            statusHtml = (<div>
                <button className='widgetButton statusButton' id="statusBtn" onClick={showStatus}>&nbsp;!&nbsp;</button>
                <div className="snackbar " id="statusSnackbar">{statusMessage}</div>
            </div>
            )
        }


        // logic for handling the location display; swap out the specific HTML as needed
        // also there's gotta be a better way to do this logic
        let locationHtml;
        
        if (bestLocation) {
            // if there's a best location, show it (means closest and most recent were the same and not blank)
            locationHtml = (<div>
                <button className='widgetButton' id="bestButton" onClick={showBest}>Best Location</button>
                <div onClick={() => copyLocation(bestLocation)} className="snackbar " id="bestSnackbar">{bestLocation}</div>
            </div>)
        } else if (closestLocation && recentLocation) {
            // if there isn't a best location (b/c of the 'else') but closest and recent are truthy, they must be different (show both)
            locationHtml = (<div>
                <button className='widgetButton' id="closestButton" onClick={showClosest}>Closest Location</button>
                <div onClick={() => copyLocation(closestLocation)} className="snackbar " id="closestSnackbar">{closestLocation}</div>
                &nbsp;
                <button className='widgetButton' id="recentButton" onClick={showRecent}>Previous Location</button>
                <div onClick={() => copyLocation(recentLocation)} className="snackbar " id="recentSnackbar">{recentLocation}</div>
            </div>)
        } else if (closestLocation) {
            // this happens if closest and recent were different, but recent was falsy, meaning it was blank (show closest only)
            locationHtml = (<div>
                <button className='widgetButton' id="closestButton" onClick={showClosest}>Closest Location</button>
                <div onClick={() => copyLocation(closestLocation)} className="snackbar " id="closestSnackbar">{closestLocation}</div>
            </div>)
        } else if (recentLocation) {
            // this happens if closest and recent were different, but closest was falsy, meaning it was blank (show recent only)
            locationHtml = (<div>
                <button className='widgetButton' id="recentButton" onClick={showRecent}>Previous Location</button>
                <div onClick={() => copyLocation(recentLocation)} className="snackbar " id="recentSnackbar">{recentLocation}</div>
            </div>)
        } else {
            // this means best, recent, and closest locations were all falsy (very likely blank); show an error or something, probably a reset button too
            // may want to change this later, but the most elegant solution might just be to show nothing
            // locationHtml = (<div>
            //     {/* <span className='widgetText'>
            //         LOCATION SERVICES FAILED
            //     </span> */}
            // </div>)
        }

        return(
            <div id="widget" className='widgetBox boxShadowImitation' style={{
                backgroundImage: `url(${imgUrl})`
            }}>
                <button className='widgetButton resetButton' onClick={requestRecommendation}>&#8635;</button>
                <span className='widgetText'>
                    {itemName}
                </span>
                <br/>
                <br/>
                {statusHtml}
                {locationHtml}
                <br/>
                <br/>
            <button onClick={clickOrder} className='widgetButton' id="orderSpan">Order Now</button>
            </div>
        )
    }

    // fail display (if rec fails completely)

    else if (status == "fail")
    {
        return(
            <div className='widgetBox boxShadowImitation' style={{
                backgroundImage: `none`}}>
                <span className='widgetText' style={{fontSize: "1.5rem"}}>
                    {failMessage}
                </span>
                <br/>
                <br/>
                <button className='widgetButton' style={{
                    //   background: '#a83232'
                }} onClick={requestRecommendation}>Retry</button>
            </div>
        )
    }

    // may want to add more nuances, like having messages for showing location/time failure on the success display or something
}

export default WidgetIntegrated;