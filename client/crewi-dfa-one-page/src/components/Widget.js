import React, { useEffect, useState } from 'react'

const Widget = (props) => {
    //these happen once no matter what; they will not run again
    const [username, setUsername] = useState("");
    const [status, setStatus] = useState("loading");
    const [timeSlot, setTimeSlot] = useState("");
    const [imgUrl, setImgUrl] = useState("");
    const [itemName, setItemName] = useState("");

    let time = "";
    let timeStatus = "";
    
    //this runs the first time, and then again whenever username is changed 
    useEffect(() => {
        timeStatus = "";
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

                setImgUrl(result.recommendations[0].imgUrl);
                setItemName(result.recommendations[0].name);

                setStatus("success");
            }).catch(error => {
                // logs the error, updates state to fail
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
            
            // request options were needed for the API, we'd only ever need get anyways
            var requestOptions = {
                method: 'GET',
            };        

            // returns the address to requestRecommendation, takes in coordinates and options
            return await getAddress(result.coords.latitude, result.coords.longitude, requestOptions);
        } catch {
            setStatus("no-location loading");
            return "";
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

    // takes coordinates, returns street address
    const getAddress = async function(latitude, longitude, requestOptions) {
        // need to add a reject procedure, small edits to be made to this
        const addressPromise = new Promise((resolve, reject) => {
            fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${latitude}&lon=${longitude}&apiKey=a9868a78354f43f0a3574acd600e2ceb`, requestOptions)
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    // resolving this will basically make it go into addressPromise
                    resolve(result.features[0].properties.formatted);
                }).catch(error => reject(error))
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
        // only proceed if the user actually picks a time slot; otherwise, just ignore the submit until they do
        if (timeSlot != "") {
            console.log('form submitted');
            timeStatus = "time slot selected";
            // because the requesting useEffect only runs on username change, request has to be called again
            requestRecommendation();
        }
    }

    // contains overarching logic for loading data, requesting recommendation, and updating status accordingly
    const requestRecommendation = async function() {
        // requesting is when the widget is "loading"
        setStatus("loading");

        // if time slot is blank, try to request with time loading
        if (timeStatus == "") {
            try {
                // if this fails, no time is invoked
                time = loadCurrentTime();

                try {
                    // grabs location (meaning street address) and waits here so that fetchRec won't get called until this done
                    // loadCurrentLocation needs to return a blank or sentinel value into location if something fails
                    let location = await loadCurrentLocation();
    
                    // this will actually grab the rec and update the status for the DOM
                    fetchRecommendation(username, time, timeSlot, location);
                
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
            console.log("TIMESLOT: " +timeSlot);
            // this will run if time failed and the user picked a time slot
            try {
                // grabs location (meaning street address) and waits here so that fetchRec won't get called until this done
                // loadCurrentLocation needs to return a blank or sentinel value into location if something fails
                let location = await loadCurrentLocation();

                // this will actually grab the rec and update the status for the DOM
                fetchRecommendation(username, time, timeSlot, location);
            } catch (error) {
                console.log(error);
                // if something goes wrong, display fail
                setStatus("fail");
            }
        }

        // time slot needs to be reset after each request so that loading time will be re-attempted
        
    }

    const clickWidget = () =>{
        console.log('test')
    }

    // DISPLAY SECTION

    // loading display
    if (status == "loading")
    {
        return(
            <div onClick={clickWidget} className='widgetLoading widgetBox boxShadowImitation' style={{
                backgroundImage: `url(https://drive.google.com/uc?export=view&id=1jOKIa9urkCFsa6OGGf8Hrd8DROPzkmfa)`
            }}>
            </div>        
        )
    }

    else if (status == "no-location loading")
    {
        return(
            <div onClick={clickWidget} className='widgetLoading widgetBox boxShadowImitation' style={{
                backgroundImage: `url(https://drive.google.com/uc?export=view&id=1jOKIa9urkCFsa6OGGf8Hrd8DROPzkmfa)`
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
        return(
            <div onClick={clickWidget} className='widgetBox boxShadowImitation' style={{
                backgroundImage: `url(${imgUrl})`
            }}>
                <span className='widgetText'>
                    {itemName}
                </span>
                <br/>
                <br/>
                <br/>
                <br/>
                <br/>
            <button className='widgetButton' id="orderSpan">Add to Cart</button>
            </div>
        )
    }

    // fail display (if rec fails completely)

    else if (status == "fail")
    {
        return(
            <div className='widgetBox boxShadowImitation' style={{
                backgroundImage: `none`}}>
                <span className='widgetText'>
                    Recommendation failed
                </span>
                <br/>
                <br/>
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

export default Widget;