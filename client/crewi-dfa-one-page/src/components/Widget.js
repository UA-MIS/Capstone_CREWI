import React, { useEffect, useState } from 'react'

const Widget = (props) => {
    //these happen once no matter what; they will not run again
    const [username, setUsername] = useState("");
    const [status, setStatus] = useState("loading");
    const [timeSlot, setTimeSlot] = useState("");
    
    let time = "";
    
    //this runs the first time, and then again whenever username is changed 
    useEffect(async () => {
        requestRecommendation();
    }, [username])

    // fetches the recommendation, might need to be async? doesn't look like it does at the moment
    const fetchRecommendation = function(username, time, timeSlot, location) {
        // fix this hard-coded URL later
        fetch(`http://localhost:8000/recommendation/`, {
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
              location: location  
            })
        })
            .then(response => response.json())
            .then(result => {
                // logs the result, updates the state (which will update the DOM)
                console.log(result);
                setStatus("success");
            }).catch(error => {
                // logs the error, updates state to fail
                console.log(error);
                setStatus("fail");
            })
    }

    //our first attempt at loading in time; it works, but we should probably reformat the time a little
    const loadCurrentTime = () => {
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
        // result will be a Geolocation object; await means execution will pause here until finished
        let result = await getCoordinates();
        
        // request options were needed for the API, we'd only ever need get anyways
        var requestOptions = {
            method: 'GET',
        };        

        // returns the address to requestRecommendation, takes in coordinates and options
        return await getAddress(result.coords.latitude, result.coords.longitude, requestOptions);
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

    // takes coordinates, returns street address
    const getAddress = async function(latitude, longitude, requestOptions) {
        // need to add a reject procedure, small edits to be made to this
        const addressPromise = new Promise((resolve, reject) => {
            fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${latitude}&lon=${longitude}&apiKey=a9868a78354f43f0a3574acd600e2ceb`, requestOptions)
                .then(response => response.json())
                .then(result => {
                    // resolving this will basically make it go into addressPromise
                    resolve(result.features[0].properties.formatted);
                })
        });

        // returns resolved/rejected result, should be the formatted address if resolved
        return await addressPromise;
    }

    //this runs whenever state or props are updated; it updates token so that the useEffect above will run
    //props are updated when the button is clicked bc it will update the main state, etc.
    useEffect(() => {
        setUsername(props.username);
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

        // because the requesting useEffect only runs on username change, request has to be called again
        requestRecommendation();
    }

    // contains overarching logic for loading data, requesting recommendation, and updating status accordingly
    const requestRecommendation = async function() {
        // requesting is when the widget is "loading"
        setStatus("loading");

        // need to break this error-handling up for now, at the moment if something goes wrong it'll go to no-time mode
        try {
            // load time, small chance this needs to be async but getting time is usually instant
            time = loadCurrentTime();
            // grabs location (meaning street address) and waits here so that fetchRec won't get called until this done
            // loadCurrentLocation needs to return a blank or sentinel value into location if something fails
            let location = await loadCurrentLocation();

            // this will actually grab the rec and update the status for the DOM
            fetchRecommendation(username, time, timeSlot, location);
        
        } catch (e) {
            // if something goes wrong, go into no-time mode (again, restructure this later)
            setStatus("no-time");
        }
    }

    // DISPLAY SECTION

    // loading display
    if (status == "loading"){
        return(
            <div>
                <h1>Loading</h1>
            </div>
        )
    }

    // no-time display

    else if (status == "no-time")
    {
        return(
            <div>
                <hr></hr>
                <span>Username: </span>
                <span>{username}</span>
                <br></br>
                <hr></hr>
                <br />
                <hr />
                <span>We couldn't load your current time please select an option below:</span>
                <br />
                <form onSubmit={formSubmit}>
                            <div className="radio">
                                <label>
                                    <input
                                        type="radio"
                                        value="Morning"
                                        name="dayPart"
                                        checked={timeSlot == "Morning"} 
                                        onChange={onValueChange}
                                    />
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
                                    />
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
                                    />
                                    Night
                                </label>
                            </div>
                            <div>
                                Selected option is : {timeSlot}
                            </div>
                            <button className="btn btn-default" type="submit">
                                Submit
                            </button>
                        </form>                
            </div>
        )
    }

    // success display (if rec is loaded successfully)

    else if (status == "success")
    {
        return(
            <div>
                <h1>SUCCESS</h1>
            </div>
        )
    }

    // fail display (if rec fails completely)

    else if (status == "fail")
    {
        return(
            <div>
                <h1>FAIL</h1>
            </div>
        )
    }

    // may want to add more nuances, like having messages for showing location/time failure on the success display or something
}

export default Widget;