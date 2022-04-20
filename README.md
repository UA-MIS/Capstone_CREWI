### CLOSE-OUT UPDATE

In our close-out meeting, we decided to make this repo public. This will not cause any issues, but it does mean updating the widget is much easier.

Rather than needing to use the crewiStaticFiles repo, the widget static files can be accessed directly via this repo (because it is public). To implement this change, just update the CDN URLs in the embedded widget and public/index.html of the one-page. This change is particularly nice because it also means there's no need to push to the crewiStaticFiles repo when updating the widget. The instructions will be kept in the ReadMe for now in case access changes, but a future project team could remove that section of the documentation and delete the crewiStaticFiles repo if desired.





### Capstone_CREWI Codebase

Before developing, be sure to watch and follow the setup video.

To access the codebase, use the capstonecrewi Github account:


Email: capstonecrewi@gmail.com

Username: capstonecrewi

Password: CapstoneCREWI2022!


The Capstone_CREWI repo has the code for the project, but the crewiStaticFiles repo is also necessary for updating the widget (discussed in more detail in the widget ReadMe).

For questions, reach out to me via email at stward1@crimson.ua.edu


### Current State of Deployment

Right now, there is a Heroku server for the engine and one for the one-page. The widget is "hosted" via the crewiStaticFiles repo. The servers are currently down; use the Capstone CREWI credentials to sign into Heroku and deploy them again.

The MySQL database is hosted already; use the credentials in the .env file (or from the configuration variables in engine Heroku server) to connect and view the data as needed.
