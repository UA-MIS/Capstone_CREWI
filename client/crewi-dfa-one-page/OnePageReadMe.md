### CREWI DFA One-Page ReadMe

This is the Dude-fil-A one-page. 


### Running the One-Page

To run the one-page locally, do the following:
1. `npm install` to install the dependencies
2. `npm start` to run the one-page locally


### `npm install`

Installs all the dependencies for the one-page.


### `npm start`

Runs the one-page locally. This is good for developing features and testing. Open http://localhost:3000 to view it in your browser.


### Integrated Widget

Uncomment the WidgetIntegrated component in MainComponent.js to use the integrated widget. The integrated widget is the version with the actual functionality built-in (rather than embedding the widget as a separate React app). Make sure to comment out the WidgetEmbedded code; only either WidgetIntegrated or WidgetEmbedded should be uncommented at once.


### Embedded Widget

Uncomment the WidgetEmbedded component in MainComponent.js to use the embedded widget. The embedded widget is the version that loads in the static widget files using the jsDelivr CDN (rather than integrating the widget as another React component). Make sure to comment out the WidgetIntegrated code; only either WidgetEmbedded or WidgetIntegrated should be uncommented at once.