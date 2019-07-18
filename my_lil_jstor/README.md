# Technical Exercise Goals

This exercise is not meant to test how fast you get to solutions, but to see what your thought process
is when tackling problems such as these. Writing code that represents your best practices is more important than writing
code that works and fulfills the success criteria. Several developers at JSTOR will be available via the
Slack room that you have been invited to in order to support questions that you may have along the way.

Please fork the repo to get started and when you think you are finished, issue a pull request. Preferably
this will be done before your in-person interview so that we can go over the code and start a dialog with
you about it when you are here.

Thank you and we hope that you find this exercise fun and challenging. :)

# My Lil' JSTOR

My Lil' JSTOR is a great product we are planning on rolling out to our younger audience. On the site, a user can
purchase coloring books from our collection for a flat rate of $5. The application was started a while ago and
is in need of a few updates before we can officially launch. Luckily, the developers that created the app left us a
few instructions to get started. Check out the setup steps to see if you can get the app going and
try to add the new features requested from the product owner.


## Setup

### Python
My Lil' JSTOR is written in Python 3 and utilizes the [Django framework](https://www.djangoproject.com/).
The [Django installation guide](https://docs.djangoproject.com/en/1.11/intro/install/) provides a detailed guide
for creating the necessary environment. Although not required, it may help to load the project into
[PyCharm](https://www.jetbrains.com/pycharm/) to assist with seeing the overall project structure and running the app.

Once all dependencies are resolved, we can run some commands to initialize the application and start the server.

To create a local SQLite database with test data
```
python manage.py migrate
```

To start the My Lil' JSTOR server
```
python manage.py runserver
```

### Javascript & SASS
Javascript and SASS live in the `my_lil_jstor/static/` directory and can be built with
[webpack](https://webpack.github.io/), an npm package used for bundling code. This means you will have to download
and install [nodejs](https://nodejs.org/en/), which will also bring in npm.

These assets are built using an in-house front end framework called Bonsai, which is based off of
[Foundation](https://foundation.zurb.com/). The [Bonsai Styleguide](https://www.jstor.org/styleguide) includes
examples of various components and display helpers that may be useful when creating features.

To install the necessary dependencies
```
npm install
```

If the above command fails because you installed python 3, and you're on a mac, try the following to use python2
```
npm install --python=/usr/bin/python
```

To transpile and package the static assets
```
npm run build
```

## Tasks

Below are some tasks to complete ahead of the interview. Please feel free to create test cases as necessary. We will go
over the code with you to discuss design choices and ask questions.

### Something is Broken!

We have several coloring book pages ready for our users, but there appears to be a problem with the page.
Navigate to the homepage and click on the "featured book" to see the problem. We are pretty sure
that all the code that is needed to fix the problem exists in the repo already, so maybe we just aren't
calling it where we should be...

Success Criteria:
* Users are able to see Coloring Book details again

### Browse

We need a browse page so all our lil' JSTOR users can see the various coloring books on the site.

Success Criteria
* Users can see all the coloring books we have available to read
* Users can see the image, title and description for each book
* Clicking on a book image or title will go to the book details page

### User Comments

Our users love the coloring books and want to leave comments about how great they are.
We need to create a form on the coloring book details page to submit a new comment.
This form requires the name and comment section to be populated, and have an option to supply a rating of 1 to 5.
Users should not be able to submit a comment to the server if the required fields are blank. We would like to print out
the comments with the submitted fields on the book details page.

Success Criteria
* Users can submit a comment on the book details page
* Name and comment are required before submitting form to server
* Review of 1 to 5 is optional
* Users can see old comments on the details page

### Likes

We want the ability for users to give feedback about the title by posting a "Like" to a book.
Users should be allowed to like as many books as they want but we should do our best to limit each session to
like each book only once. We also want to display how many likes a book as on the page.

Success Criteria
* User is able to 'Like' a book
* User can see how many 'Likes' a book currently has
* User is prevented from re-liking a story if they are using the same browser


### Discounts

We would love to offer discounts to our most popular coloring books. Currently, each coloring book is $5 and we can now
offer discounts of $.25 off for every like a book gets and $.50 off for each comment a book gets. The minimum price we can offer for each book is $2.50.
On the book details page we need to show the updated price to the user. 

Success Criteria
* Discounts are: 
    - $.25 per like
    - $.50 per comment
* Minimum price per book is $2.50
* Updated price is displayed on the page
