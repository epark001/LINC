# Business Logic Server Template

A template server for business logic integration with the Clinc AI platform.

# Dependencies
- [node](https://nodejs.org/en/download/)
- [npm](https://www.npmjs.com/get-npm)

# Start the server locally
```
npm install
npm start
```

# Business Logic Interface
A user can insert arbitrary Business Logic into a custom competency by using a webhook. In this section, we will discuss setting up a webhook, including how to use it to insert and edit the variables that are used for response generation.

## Business Logic Setup
1. In the upper right hand corner of the Clinc AI Platform, click on the dropdown menu that is labeled with the user's username.
2. In the dropdown, click on the *Settings* tab.
3. Once on the settings page, enter the webhook URL into the appropriate input box.
4. Check off the competencies that the user would like to invoke business logic for,
