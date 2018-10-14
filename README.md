# Votingbooth
Need to vote on something? Step right up to the votingbooth and cast your vote. Are you doing your part?

## Overview

The votingbooth is a python web-application to create polls and vote in them. Votes can be cast either anonymously or as a registered user, but all cast votes are anonymous regardless of login status.

Checkout the app att <https://fgronqvist-votingbooth.herokuapp.com/> and the repo at <https://github.com/fgronqvist/votingbooth>

The specifications for the application is listed at <http://advancedkittenry.github.io/suunnittelu_ja_tyoymparisto/aiheet/Aanestys.html>. [Usecases](documentation/userstories.md), object-diagrams, database schema layouts and definitions will be added as the work progresses.

Check out the [documentation](documentation) for further details.

## Datastorage

The back-end data-storage is a Sqlite/Postgres database with a schema pictured below.

![db diagram](documentation/Db_diagram.png)

## Application layout

The app is structured in the way below.

  .
  |-- application
  |   |-- account
  |   |-- admin
  |   |-- poll
  |   |-- static
  |   |   |-- css
  |   |   |   `-- images
  |   |   |-- img
  |   |   `-- js
  |   |       `-- i18n
  |   |-- templates
  |   |   |-- account
  |   |   |-- admin
  |   |   |-- poll
  |   |   `-- vote
  |   `-- vote
  `-- documentation

### Documentation

The documentation holds the files (md-formatted) and images for any documentation that is not included in this README.md.

For such a simple app as this one, a separate documentation directory is a bit overkill, but I thought it would be good practice to keep some parts separated (like the weekly progress-reports).

### Account

The account module holds forms, models and views that deal with things like:

 * account registration
 * login
 * user roles
 * db queries regarding the account or account_role tables

A rule of thumb, if something needs to do something with the account, it probably belongs in here.

### Admin

The admin module holds mostly views that require the "ADMIN" role. As it currently stands, all models it requires are imported from the other modules (like account/models or poll/models) to keep the db functionality (basically the schema and some grouping queries) in a single model. 

This is basically to try to prevent features from "sprawling" db queries all over the place.

The module handles things like:

 * showing total account/poll/vote information
 * showing top lists of polls and accounts


### Poll

The poll module handles forms, models and views with regards to polls (but not voting on polls). Basically functions like:

 * creating, updating and deleting polls
 * creating, updating and deleting voting options (alternatives one can vote on)

If something has to do with a specific poll, it probably belongs in this module.

### Static

This "module" (actually just a normal directory) houses all static files of the user interface. Logos/images, javascript (js) and css files all go in here. The css/images directory is because a 3rd party js library had it setup that way and I didn't want to mess with it. The actual user interface images go into "static/img".

Lots of projects prefer to use CDN (content delivery networks) for these (mostly js and css) libraries, but I kind of prefer to have the libraries as part of the project. This will ofcourse have an effect on really heavy traffic sites in bandwith usage, but for smaller apps like this one it doesn't allways make sense. A 3rd party CDN will be an extra dependency that you probably don't want in the long run. If your app is in internal use for some company, it might run for 10+ years without needing any changes to it, but a CDN might drop the url without any prior notice. Scouring the interwebs for a 10 year old js library is probably not something anybody should have to do.

## Templates

As I understand Flask (as of writing this on 2018-10-14), this is the default template setup. You have this templates folder and you dump the modules templates in here, so I made the templates folder mimic the modules structure. So any module specific templates go into a folder named after the module. Any "general" templates stay on the "templates/" level.

This helps a bit with naming conflicts (poll/index.html vs account/index.html) and helps to keep them a bit more "grouped together" around the same theme. One could ofcourse use a naming convetion (like poll_index.html), but that might get screwed up at some point.

Flask seems to have "blueprints" and you could place the templates under the modules, but as far as I've understod it would still require a structure like "module/template/module/index.html", which does not seem to help all that much and would basically still result in the same structure as the current template folder.

### Vote

The vote module handles the actual voting process. It is basically responsible for checking if a vote can be cast (in the selected poll) on the basis of:

 * is the poll open
 * does the poll require user registration, and if it does, is the voter logged in

It contains the forms, models and views with regards to this, so if something needs to be done with the actual voting, then this is probably the place for it.

# Postscript and license

This app is a course-excercise, so this will probably not be developed further by me (as I am completly swamped with other things). You are very welcome to pull any bits and pieces you might find helpful in your own projects, or even fork the whole thing. I will probably not be able to pull any merge requests tho.

I will update this if things change. Thanks for your interest and have a good one!

Copyright (c) 2018 F. Grönqvist (https://github.com/fgronqvist/)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

 
