This repository is a modification of: https://github.com/openai/gpt-2 for our specific purposes

# Purpose
The objective of this API is to provide the 3 best possible responses to sentences that the user would input via http GET request as a parameter. This API that can help developers use GPT2 for their web application projects without the hassle of figuring out how GPT2 works. 

This API was used in a dating app project, where given the sentences the users exchanged the API had to suggest following up questions to keep the flow of the conversation going.

# How it works?
This web API manages inputs and outputs with HTTP GET requests. The developer should wrap the users sentence in an URL in the following way:

```
http://localhost:5000/?bio=[user sentence]
```
Example:

```
http://localhost:5000/?bio=i%20like%20to%20exercise
```

The output of this API is in JSON format under the "sentences" field as a list of strings of size 3. This is a response from the previous GET request.

# How to run?
1. First open the project in your favorite IDE
2. Execute the python script where the flask API runs (app.py) using this command

```
flask run
```

You can use other parameters as --port to modify the default deployed port which is 5000

3. Wait until the API is running and test URL with Postman or your favorite browser

# Walkthrough
<img src="GPT2.gif"/>

Authors: Paulina Acosta, Usman Tariq, Michael Duboc
