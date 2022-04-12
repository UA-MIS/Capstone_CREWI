### CREWI Client ReadMe

This folder contains all the front-end stuff for the CREWI project. Right now, that means the widget itself and the Dude-fil-A one-page application. Refer to WidgetReadMe.md and OnePageReadMe.md for more details on each.

Make sure to refer to the setup video before running either the one-page or widget to install the necessary software (though node.js should be sufficient).


### How the Front-End is Designed

The one-page and widget are just standard React apps. However, the one-page implements the widget using a Content Delivery Network (CDN). Technically, there's a version with an integrated or embedded widget, but that's explained in more detail in the one-page ReadMe. The important thing to understand here is how the CDN enables the one-page and widget to interact:

The one-page uses CDN requests like this: https://cdn.jsdelivr.net/gh/capstonecrewi/crewiStaticFiles/static/js/main.a9ffa889.js

The format here is the jsDelivr Github request format; gh is for Github, then the username, then the repo name, then the path to the file. In this case, that's the main JavaScript build file for the widget. Whenever you change the widget, you'll need to update static files in this "crewiStaticFiles" repo and update the requests if the file names changed (this is explained in the widget ReadMe).

The one-page uses these requests to load in the widget files; this is possible regardless of the front-end technology being used. In other words, any front-end can load in the widget as an embedded HTML element with CDN requests.