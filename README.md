# Business Logic Server Template

A template server for business logic integration with the Clinc AI platform.

# Dependencies
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/)


# Start the server locally
```
docker-compose up
```
# Start the server on Heroku
1. Create an app on Heroku.
2. In the `Settings` page of the heroku app, configure the app to use the default stack (currently `heroku-16`) and the python buildpack.
3. In the `Deploy` page of the app, configure the app to be connected to this github repo.
4. Add the URL of the heroku app to the ALLOWED_HOSTS list in `my_project/settings.py`
5. Push to the github repo and deploy the heroku app. You can either configure the heroku app to automatically deploy on every push to a branch or manually deploy.
6. Configure in the Clinc Platform to connect to the heroku app. Refer to the documentation in the Clinc Platform for details.


# Business Logic Interface

A user can insert arbitrary Business Logic into a custom competency by using a webhook.  In this section, we will discuss setting up a webhook, including how to use it to insert and edit the variables that are used for response generation.

Business Logic Setup
------------------------------
1. In the upper right corner, click on the drop-down menu that is labeled with the user's username.
1. In that drop-down, click on the *Settings* tab.
1. Once on the settings page, enter the webhook URL into the appropriate input box.
1. Check off the competencies that the user would like to invoke business logic for.

## Business Logic Request

On every request, the platform will check (1) if the user has Business Logic set up, and (2) whether the current Competency is enabled with Business Logic.  If both conditions are true, it will call the user's Business Logic with a request similar to the following:

```
POST /<BL-URL> HTTP/1.1
{

    "qid": "6d090a7e-ba91-4b49-b9d5-441f179ccbbe",
    "lat": 42.2730207,
    "lon": -83.7517747,
    "state": "transfer"
    "dialog": "lore36ho5l4pi9mh2avwgqmu5mv6rpxz/98FJ",
    "device": "web",
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "time_offset": 300,
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "values": [
                {
                "tokens": "John's checking account",
                "resolved": -1
                }
            ]
        },
        "_ACCOUNT_TO_": {
            "type": "string",
            "values": [
                {
                "tokens": "credit card",
                "resolved": -1
                }
            ]
        },
        "_TRANSFER_AMOUNT_": {
            "type": "string",
            "values": [
                {
                "tokens": "$400",
                "resolved": -1
                }
            ]
        }
    }
}
```

### Explanation of Business Logic payload keys:

  * `lat` : Latitude of the query origin.
  * `qid` : Query ID.
  * `lon` : Longitude of the query origin.
  * `state` : The state that the classifier predicted for the current query.
  * `dialog` : The dialog token.
  * `device` : The device on which the query was made.
  * `query` : The query that was made.
  * `time_offset` : The time zone offset from UTC.
  * `slots` : The slots that were extracted for the query.

The only mutable fields in the business logic payload are `slots` and `state`, which will be explained in more detail below.

### Explanation of `slot` dictionary:

  * `values` : A list of dictionaries, one for each instance of the slot extracted form the user query.
  * `type` : The type of the data in the slot.  The possible values `string`, `date`, `number`, or `money`.

### Explanation of `values` dictionary:

  * `tokens` : The original tokens that were extracted from the user query.
  * `resolved` : Whether an extracted token has already been resolved.  Slots extracted from a user's query for the first time will be sent with a `"resolved": -1`.  There are three possible values that can be returned:  `-1` for unresolved,  `0` for unsure, and `1` for already resolved. These will be explained in more detail in the next section.

A response back to the platform should look similar to the following example:


```
HTTP/1.1 200 OK
{
    "lat": 42.2730207,
    "qid": "6d090a7e-ba91-4b49-b9d5-441f179ccbbe",
    "lon": -83.7517747,
    "dialog": "lore36ho5l4pi9mh2avwgqmu5mv6rpxz/98FJ",
    "device": "web",
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "time_offset": 300,
    "state": "transfer_confirm"
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "values": [
                {
                    "tokens": "John's checking account",
                    "resolved": 1,
                    "value": "College Checking Account",
                    "account_id": "353675",
                    "balance": "5824.24",
                    "currency": "USD"
                }
            ]
        },
        "_ACCOUNT_TO_": {
            "type": "string",
            "values": [
                {
                    "tokens": "credit card",
                    "resolved": 1,
                    "value": "Sapphire Credit Card Account",
                    "account_id": "7725485",
                    "balance": "332.21",
                    "currency": "USD"
                }
            ]
        },
            "_TRANSFER_AMOUNT_": {
            "type": "money",
            "values": [
                {
                    "tokens": "$400",
                    "resolved": 1,
                    "value": "400.00",
                    "currency": "USD"
                }
            ]
        }
    }
}
```

### Explanation of `values` keys:

  * `value` : [required] This is the new value the user would like to pass from the business logic back to the platform.
  *  Besides `tokens`, `resolved` and `value`, arbitrary key-value pairs can be added to the dictionary by the business logic, to pass more information to the platform. In the example shown, currency was set by the business logic.

### Examples of `resolved` statuses in `slot` responses:

If the slot is valid and you want to keep it, set `"resolved": 1`, and return it to clinc:

```
"slots": {
    "_ACCOUNT_FROM_": {
        "type": "string",
        "values": [
            {
                "tokens": "John's checking account",
                "resolved": 1,
                "value": "College Checking Account",
                "account_id": "353675",
                "balance": "5824.24",
                "currency": "USD"
            }
        ]
    }
}
```

If there are multiple possible values, and you would like the AI to try to determine which is the best match, you can send a `"resolved": 0`, along with a list of possible values inside of a `candidates` key, along with a slot mapping configuration in a `mappings` key, in the top level of the dictionary for that slot.  This will perform a slot mapping on that slot to determine the best possible match in `candidates` for the value of the slot. 

```
"slots": {
    "_ACCOUNT_TO_": {
        "type": "string",
        "candidates": [
            {
                "value": "College Savings Account",
                "account_id": "155243",
                "balance": "4521.10",
                "currency": "USD"
            },
            {
                "value": "Sapphire Credit Card Account",
                "account_id": "7725485",
                "balance": "332.21",
                "currency": "USD"
            },
            {
                "value": "401K Account",
                "account_id": "792311",
                "balance": "12554.23",
                "currency": "USD"
            }
        ],
        "mappings": [
            {   
                "children": [
                    {   
                        "threshold": 0.45,
                        "type": "phrase_embedder",
                    },  
                    {   
                        "type": "constant",
                        "value": "MAPPING NOT FOUND"
                    }   
                ],  
                "type": "first_match"
            }   
        ],  
        "values": [
            {
                "type": "string",
                "tokens": "credit card",
                "resolved": 0
            }
        ]
    }
}
```

If an identified slot doesn't quite match, or is incorrect, a `"resolved": -1` will remove the extracted slot:

```
"slots": {
    "_ACCOUNT_TO_": {
        "type": "string",
        "values": [
            {
                "tokens": "credit card",
                "resolved": -1,
                "reason": "You do not have a credit card with us."
            }
        ]
    }
}
```

A user adding their own slots:

To add your own slots that can be used in the Jinja response templates, simply add a new key into the `slots` dictionary with a structure similar to the other slots.  An example with the added slot `TRANSFER_FEE` can be found below:

```
HTTP/1.1 200 OK
{
    "lat": 42.2730207,
    "qid": "6d090a7e-ba91-4b49-b9d5-441f179ccbbe",
    "lon": -83.7517747,
    "dialog": "lore36ho5l4pi9mh2avwgqmu5mv6rpxz/98FJ",
    "device": "web",
    "query": "I want to transfer $400 from John's checking account to my credit card account.
    "time_offset": 300,
    "state": "transfer_confirm"
    "slots": {
        "_ACCOUNT_FROM_": {
            "type": "string",
            "values": [
                {
                    "tokens": "John's checking account",
                    "resolved": 1,
                    "value": "College Checking Account",
                    "account_id": "353675",
                    "balance": "5824.24",
                    "currency": "USD"
                }
            ]
        }
        "_ACCOUNT_TO_": {
            "type": "string",
            "values": [
                {
                    "tokens": "credit card",
                    "resolved": 1,
                    "value": "Sapphire Credit Card Account",
                    "account_id": "7725485",
                    "balance": "332.21",
                    "currency": "USD"
                }
            ]
        },
        "_TRANSFER_AMOUNT_": {
            "type": "money",
            "values": [
                {
                    "tokens": "$400",
                    "resolved": 1,
                    "value": "400.00",
                    "currency": "USD"
                }
            ]
        },
        "_TRANSFER_FEE_": {
            "type": "money",
            "values": [
                {
                    "tokens": "$5.00",
                    "resolved": 1,
                    "value": "5.00",
                    "currency": "USD"
                }
            ]
        }
    }
}
```


Upon a successful response from a Business Logic server, the new set of variables will be directly passed into the user's response templates, allowing them to customize their responses with the new slots introduced in the Business Logic.

Business Logic Transitions
------------------------------

Business Logic transitions can be made by overwriting the `state` key in the Business Logic payload.  There must be an existing Business Logic transition between the state the user was previously in, and the state to which they are trying to transition. These transitions can be configured via the state graph editor for the relevant competency.

# Adding your own business logic

To add your own business logic to this server, simply add to `/my_project/my_app/views.py`.

`/my_project/my_app/views.py` is an example view.  Only `views.py` is used by the business logic server.
