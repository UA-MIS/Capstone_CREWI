import React, { Component } from 'react';

export default class Header extends Component {

    render() {
        return(
                <span>The Widget goes here</span>
        )
    }

}
// export interface AppProps {
//     id: string;
// }

// export default class WidgetComponent extends Component {

// const App: React.FC<AppProps> = ({ id }) => {
//     constWrapper HTMLElement | null document.getElementById(id);

//     const ownerData: string = wrapper
//      ? ((wrapper as HTMLDivElement).getAttribute("owner-data") as string)
//      : "";
// };


//     render() {
//         return(
//            <div
//                className="App"
//                style={{
//                    boarder: "1px solid grey",
//                    padding: 24,
//                    maxWidth: 300,
//                    margin: "auto",
//                    marginTop: 24,
//                }}
//             >
//                <h1>Embedded Widget</h1>
//                <h2>Container ID</h2>
//                <h3>Owner Data:</h3>
//                <button onClick={handleClick}>A Button</button>
//            </div>
//         );
//     };

// }