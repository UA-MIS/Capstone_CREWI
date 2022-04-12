### CREWI Widget ReadMe

This is the CREWI Widget. It can embedded in any front-end by loading in a few of the static files. Note that the one-page is not part of this; the widget and one-page are two separate React apps.


### Running the Widget

To run the widget locally, do the following:
1. `npm install` to install the dependencies
2. `npm start` to run the widget locally


### Updating the Widget

In order for changes on the widget to be reflected on the one-page, make sure to do the following:
1. Use `npm run build` to build the updated widget
2. Check the terminal for which files are needed (expect three files)
3. Go to the one-page and update the file names (they may or may not be different) at index.html in crewi-dfa-one-page/public at the bottom of the body tag and in crewi-dfa-one-page/src/WidgetEmbedded.js
4. Only change the file names, not the whole URL (the rest is delivery via the jsDelivr CDN, discussed in the overall ReadMe.md)
5. Push the crewi-widget/build/static folder (and its contents) to this Github repo: https://github.com/capstonecrewi/crewistaticfiles
6. There are multiple ways to do this; unfortunately the separate repo is necessary because the Capstone_CREWI repo is private and the CDN can't deliver from private repos


### `npm install`

Installs all the dependencies for the widget.


### `npm start`

Runs the widget locally. This is good for developing features and testing.
c vOpen [http://localhost:3000](http://localhost:3000) to view it in your browser.


### `npm run build`

Use this to update the static files. Whenever you change stuff in the widget, make sure to run this command to update the static files. Check the terminal to see which files are needed to embed the widget (typically one JS file, a CSS file, and a chunk JS file).