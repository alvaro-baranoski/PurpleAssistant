# Purple Virtual Assistant

This code is a Flask API that is used to serve as the basis to a custom skill in the Alexa environment.

To run it you need to do the following:
- Check if skill ID changed (if you removed and created a new skill)
- run python hello.py
- run ngrok http 5000
- Get endpoint url, go to Endpoints menu in the Alexa Skill, and update the endpoint field

You can check this tutorial as a basis on how to get this done: 
https://developer.amazon.com/en-US/blogs/alexa/alexa-skills-kit/2016/06/flask-ask-a-new-python-framework-for-rapid-alexa-skills-kit-development#:~:text=Flask-Ask%3A%20A%20New%20Python%20Framework%20for%20Rapid%20Alexa,following%20interaction%20sequence%20with%20your%20Alexa-enabled%20device.%20