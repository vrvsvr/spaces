import argparse
import requests
import json
from jinja2 import Environment, FileSystemLoader

# Setup argument parsing
parser = argparse.ArgumentParser(description='Process GitHub token.')
parser.add_argument('Token', type=str, help='The token to use')
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

# Load the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/discussions.html')

def list_discussions():
    fname = "output/index.html"
    owner = 'vrvsvr'  # Example owner, replace with your desired owner
    repo = 'docs'  # Example repo, replace with your desired repo
    discussions_response = get_discussions(owner, repo)
    discussions = discussions_response['data']['repository']['discussions']['nodes']

    # Filter discussions belonging to the "Spaces" category
    spaces_discussions = [
        discussion for discussion in discussions 
        if discussion.get('category') and discussion['category'].get('name') == 'Spaces'
    ]

    # Render the template with the discussions data
    with open(fname, 'w') as f:
        html = template.render(discussions=spaces_discussions)
        f.write(html)
    # Render the template with the discussions data
    # return template.render(discussions=spaces_discussions)

if __name__ == '__main__':
    list_discussions()