import time
import logging
import requests
import secret
from openai import OpenAI

INSTAGRAM = "https://graph.facebook.com/v20.0"
client = OpenAI(
    api_key=secret.chatgpt_api_key,
)

logging.basicConfig(filename='instagram.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

negative_comments = []
negativity_check_counter = 0

def get_my_posts():    
    posts_list = []

    # 17841468212224831?fields=business_discovery.username(tariqelouzeh){followers_count,media_count,media}
    endpoint = f"/{secret.instagram_user_id}?fields=business_discovery.username(tariqelouzeh){{followers_count,media_count,media}}"
    params = {
        'access_token': secret.instagram_api_token,
    }
    
    url = f"{INSTAGRAM}{endpoint}"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        posts = response.json().get('business_discovery', {}).get("media", {}).get("data", [])
        for post in posts:
           posts_list.append(post["id"])
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.json())
    
    return posts_list


def check_post_comments(post_id):
    global negative_comments
    url = f"{INSTAGRAM}/{post_id}/comments"
    
    params = {
        'access_token': secret.instagram_api_token,
    }
    
    response = requests.get(url, params=params)
    
    logging.info(f"Listing comments for post id={post_id}")
    if response.status_code == 200:
    # Successful response, list the comments
        comments = response.json().get('data', [])
        for comment in comments:
            logging.info(f"Comment: {comment['text']}")
            logging.info("Checking if the comment is negative...")
            if is_negative(comment['text']):
                negative_comments.append([post_id, comment['text']])
                logging.warning("Comment is negative. Deleting it...")
                delete_comment(comment["id"])
                    
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.json())
    

def delete_comment(comment_id):
    time.sleep(1)
    url = f"{INSTAGRAM}/{comment_id}"
    
    params = {
        'access_token': secret.instagram_api_token,
    }

    response = requests.delete(url, params=params)

    if response.status_code == 200:
        if response.json().get("success", False):
            logging.info(f"Comment {comment_id} is deleted!")
        else:
            logging.warning(f"Failed to delete comment {comment_id}!")
    else:
        logging.error(f"Error in deleting the comment with status: {response.status_code}.")

def is_negative(comment):
    global negativity_check_counter
    prompt = "Does this sentence have negative, aggressive, hateful or discouraging language? Say yes or no: \n"
    prompt += comment
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    negativity_check_counter = negativity_check_counter + 1
    answer = response.choices[0].message.content.lower().strip()
    if len(answer) > 2:
        return answer[:3] == "yes"
    else:
        return False

def generate_report():
    logging.info(f"\n\n--------------REPORT--------------")
    logging.info(f"Checked {negativity_check_counter} comment and found {len(negative_comments)} negative comments.\n")
    for comment in negative_comments:
        logging.info(f"Post: {comment[0]} | Comment: {comment[1]}")
    logging.info(f"\n\n--------------END REPORT--------------")

def main():
    """
    1- Get my recent posts
    2- List all comments for a post (include comment text and id)
    3- For each comment, check positivity using chatgpt (return yes or no)
    4- delete any negative comment using comment id.
    """
    posts = get_my_posts()
    for post_id in posts:
        check_post_comments(post_id)
    
    generate_report()


if __name__ == "__main__":
    main()