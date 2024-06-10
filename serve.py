from flask import Flask, render_template, request, jsonify
import argparse
import requests
import json

parser = argparse.ArgumentParser(description='Process GitHub token.')
parser.add_argument('Token', type=str, help='The token to use')

app = Flask(__name__)
args = parser.parse_args()

HEADERS = {
    'Authorization': f'bearer {args.Token}',
    'Accept': 'application/json',
}

def get_discussions(owner, repo):
    query = """ 
    {
      repository(owner: "%s", name: "%s") {
        discussions(first: 100) {
          nodes {
            id
            title
            url
            upvoteCount
            createdAt     
            bodyHTML 
            category {
              ... on DiscussionCategory {
                name
                emoji
              }
            }
          }
        }
      }
    }
    """ % (owner, repo)

    response = requests.post('https://api.github.com/graphql', headers=HEADERS, json={'query': query})
    if response.status_code!= 200:
        raise Exception("Query failed: ", response.text)
    return response.json()

@app.route('/discussions')
def list_discussions():
    owner = 'vrvsvr'  # Example owner, replace with your desired owner
    repo = 'docs'  # Example repo, replace with your desired repo
    discussions_response = get_discussions(owner, repo)
    discussions = discussions_response['data']['repository']['discussions']['nodes']

    # Filter discussions belonging to the "Spaces" category
    spaces_discussions = [
        discussion for discussion in discussions 
        if discussion.get('category') and discussion['category'].get('name') == 'Spaces'
    ]

    return render_template('discussions.html', discussions=spaces_discussions)
    # return jsonify(spaces_discussions)

if __name__ == '__main__':
    app.run(debug=True)