import React, { useEffect, useState } from 'react'

const Widget = (props) => {
    //these happen once no matter what; they will not run again
    const [username, setUsername] = useState("");
    // const [token, setToken] = useState(props.token);
    const [status, setStatus] = useState("loading");

    const [displayName, setDisplayName] = useState("INIT");

    const [timeSlot, setTimeSlot] = useState("");
    
    let time = "";
    // let timeSlot = "";
    
    //this runs the first time, and then again whenever token is changed 
    useEffect(async () => {
        // console.log('TIME TEST');
        time = loadCurrentTime();
        let address = await loadCurrentLocation();

        console.log("TIME: " + time);
        console.log('ADDRESS: ' + address);
        try {
            throw 'exception'
            fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${result.coords.latitude}&lon=${result.coords.longitude}&apiKey=a9868a78354f43f0a3574acd600e2ceb`, requestOptions)
            .then(response => response.json())
            .then(result => console.log(result.features[0].properties))
              .then(() => {
                fetch('https://randomuser.me/api')
                .then(response => {/*console.log(result);*/ return response.json();})
                .then(data => {
                    console.log(data);
                    setDisplayName(data.results[0].name.first);
                    setStatus("done");
                    // testFunction();
                }).catch(error => {
                    console.log(error);
                    setStatus("failed");
                })
              })
            .catch(error => console.log('error', error));
        
        } catch (e) {
            // console.log('excepting');
            setStatus("no-time");
        


        }

        //about 90% sure this will force location to happen before the fetch request
        const promise = new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
          });
        
        let result = await promise;
        
        var requestOptions = {
            method: 'GET',
          };
          
        //this should wait on the resolution of the geolocation
        //then it'll get the address
        //then it'll call the other API (not related, just for testing purposes)


        // console.log(result);

    }, [username])

    const testFunction = () => {
        setStatus("done");
    }

    const requestRecommendation = function(username, time, timeSlot, location) {
        fetch(`http://localhost:8000/recommendation/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
              username: username,
              time: time,
              timeSlot: timeSlot,
              location: location  
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            })
    }

    //our first attempt at loading in time; it works, but we should probably reformat the time a little
    const loadCurrentTime = () => {
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

    const loadCurrentLocation = async function() {
        let result = await getCoordinates();
        
        var requestOptions = {
            method: 'GET',
        };        

        return await getAddress(result.coords.latitude, result.coords.longitude, requestOptions);
    }

    const getCoordinates = async function() {
        const coordinatePromise = new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });
        
        return await coordinatePromise;
    }

    const getAddress = async function(latitude, longitude, requestOptions) {
        const addressPromise = new Promise((resolve, reject) => {
            fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${latitude}&lon=${longitude}&apiKey=a9868a78354f43f0a3574acd600e2ceb`, requestOptions)
                .then(response => response.json())
                .then(result => {
                    resolve(result.features[0].properties.formatted);
                })
        });

        return await addressPromise;
    }

    const resetToLoading = () => {
        setStatus("loading")
    }

    //this runs whenever state or props are updated; it updates token so that the useEffect above will run
    //props are updated when the button is clicked bc it will update the main state, etc.
    useEffect(() => {
        setUsername(props.username);
    })

    const onValueChange = (event) => {
        setTimeSlot(event.target.value);
    }

    const formSubmit = (event) => {
        event.preventDefault();
        console.log(timeSlot);
        setStatus("loading");
        callMe();
    }

    const callMe = async function() {
        // console.log('TIME TEST');
        time = loadCurrentTime();
        let location = await loadCurrentLocation();

        console.log("TIME: " + time);
        console.log('ADDRESS: ' + location);
        try {
            requestRecommendation(username, time, timeSlot, location);

            // throw 'exception'
            // fetch(`https://api.geoapify.com/v1/geocode/reverse?lat=${result.coords.latitude}&lon=${result.coords.longitude}&apiKey=a9868a78354f43f0a3574acd600e2ceb`, requestOptions)
            // .then(response => response.json())
            // .then(result => console.log(result.features[0].properties))
            //   .then(() => {
                // fetch('https://randomuser.me/api')
                // .then(response => {/*console.log(result);*/ return response.json();})
                // .then(data => {
                //     console.log(data);
                //     setDisplayName(data.results[0].name.first);
                //     setStatus("done");
                //     // testFunction();
                // }).catch(error => {
                //     console.log(error);
                //     setStatus("failed");
                // })
            //   })
            // .catch(error => console.log('error', error));
        
        } catch (e) {
            console.log('excepting');
            setStatus("no-time");
        


        }

        //about 90% sure this will force location to happen before the fetch request
        const promise = new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
          });
        
        let result = await promise;
        
        var requestOptions = {
            method: 'GET',
          };
          
        //this should wait on the resolution of the geolocation
        //then it'll get the address
        //then it'll call the other API (not related, just for testing purposes)


        // console.log(result);

    }

    if (status == "loading"){
        return(
            <div>
                <h1>Loading</h1>
            </div>
        )
    }
    else if (status == "no-time")
    {
        return(
            <div>
                <hr></hr>
                <span>Username: </span>
                <span>{username}</span>
                <br></br>
                <hr></hr>

                {/* this will show the username of the main component; props can be used to grab parent state info */}
                {/* since the parent changing would mean the child is re-rendered, this is updated dynamically (useEffect and some of the hooks work a little differently, refer to the Reddit widget stuff for details) */}
                {/* the same dynamic stuff is true for time */}
                <span>Time: {time}</span>
                {/* when this button is clicked, it'll call the function that increments counter but also updates time */}
                {/* <button onClick={this.displayClick}>Click Me (Clicked {this.state.counter} times)</button> */}
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

    else if (status == "done")
    {
        return(
            <div>
                {/* <span>{token}, {status}</span> */}
                <h1>{displayName}</h1>
            </div>
        )
    }
    else if (status == "failed")
    {
        return(
            <div>
                {/* <span>{token}, {status}</span> */}
                <h1>FAILED</h1>
            </div>
        )
    }
}

export default Widget;