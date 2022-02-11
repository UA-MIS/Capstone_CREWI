import React, { Component } from 'react';
import Header from './HeaderComponent';
import WidgetComponent from './WidgetComponent';
import Footer from './FooterComponent';

export default class MainComponent extends Component {

    render() {
        return(
            <React.Fragment>
                <><Header /><WidgetComponent /><Footer /></>
            </React.Fragment>
        )
    }

}