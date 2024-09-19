# instagram-negativity-manager

A small python script that integrates with Instagram API to read a professional accounts posts and their comments and then delete the comments that are found negative. The script integrates with ChatGPT API to determine if a comment is negative or not.

Prerequisites:
- Obtain tokens for Instagram API and for ChatGPT API.

- Install `openai` library
``` shell
pip3 install openai
```

Create a file called `secret.py` and add the following 3 variables:
 - `chatgpt_api_key`: ChatGPT API Key. Refer to https://platform.openai.com/docs/quickstart?context=python.
 - `instagram_api_token`: The Instagram API Token obtained from https://developers.facebook.com/
 - `instagram_user_id`: Your Instagram used id, which you can obtain from the developer account when you create the token.

Run the script by executing as a python script:
``` shell
python3 instagram.py
```
