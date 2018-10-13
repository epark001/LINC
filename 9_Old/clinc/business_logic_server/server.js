/**
 * Template Node.js Business Logic Server
 * For Clinc AI Platform
 */
'use strict';

const express = require('express');
const assignments = require('./data.json');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.use(express.json());

app.post('/', (req, res) => {
    res.setHeader('Content-Type', 'application/json');

    const state = req.body.state;
    const slots = req.body.slots;

    if(state === 'due_date') {
        // Handle business logic for the due_date competency
        if(!slots._ASSIGNMENT_) {
            // Since the due_date competency is an Informational Competency, it has an optional slot
            //  but for our purposes we want to restrict the user from moving foward until they fill
            //  that slot out
            req.body.slots._ASSIGNMENT_.values[0].resolved = -1;
        } else {
            // The slot has been provided, we can send back the due date for the specified assignment
            //  in the response
            const token = slots._ASSIGNMENT_.values[0].tokens;
            const result = assignments[token] ? assignments[token].due_date : null;
            
            if(result !== null) {
                req.body.slots._ASSIGNMENT_.values[0].resolved = 1;
                req.body.slots._ASSIGNMENT_.values[0].value = result;
            } else {
                req.body.slots._ASSIGNMENT_.values[0].resolved = 1;
                req.body.slots._ASSIGNMENT_.values[0].error = "No such assignment exists";
            }
        }

        res.send(req.body);
    } else if(state === 'get_grade_confirmed') {
        // Handle business logic for the get_grade competency
        // Since the get_grade competency is a Confirmational Competency, we can check for slots directly
        const token = slots._ASSIGNMENT_.values[0].tokens;
        const result = assignments[token].grade;

        req.body.slots._ASSIGNMENT_.values[0].resolved = 1;
        req.body.slots._ASSIGNMENT_.values[0].value = result;

        res.send(req.body);
    } else if(state === 'get_grade') {
        // Since get_grade will execute business logic for each of its intents, we should resolve the slots here
        const token = slots._ASSIGNMENT_.values[0].tokens;

        if(assignments[token]) {
            req.body.slots._ASSIGNMENT_.values[0].resolved = 1;
        } else {
            req.body.slots._ASSIGNMENT_.values[0].resolved = -1;
        }
        
        res.send(req.body);
    } else {
        console.log('No business logic for state: ' + state);
    }
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
