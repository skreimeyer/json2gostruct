# json2gostruct

json2struct reads a json file and attempts to generate sensible structs
for the go language. When dealing with unfamiliar APIs that produce deeply
nested responses, defining a data structure to unmarshal the response into is
really a nuisance. Ideally, this script will provide reasonably named structs
that require minimal tweaking for use in go source code.

If executed as main, json2gostruct will read from stdin and write to stdout for
pipelining.

Basic usage:

```
chmod +x json2gostruct.py

curl "http://some.api" | ./json2gostruct.py >> my_structs.go
```

There are a couple sticking points:

1. Arrays with divergent nested data structure will not have properly generated structs. This is papered over with a generic interface
2. The core function operates on recursion, so you could overflow your stack if you have outrageous nesting depth in the JSON file.

---

Here is the gist of what you can expect:

### input JSON

```
{
  "login": "octocat",
  "id": 583231,
  "node_id": "MDQ6VXNlcjU4MzIzMQ==",
  "avatar_url": "https://avatars3.githubusercontent.com/u/583231?v=4",
  "gravatar_id": "",
  "url": "https://api.github.com/users/octocat",
  "html_url": "https://github.com/octocat",
  "followers_url": "https://api.github.com/users/octocat/followers",
  "following_url": "https://api.github.com/users/octocat/following{/other_user}",
  "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
  "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
  "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
  "organizations_url": "https://api.github.com/users/octocat/orgs",
  "repos_url": "https://api.github.com/users/octocat/repos",
  "events_url": "https://api.github.com/users/octocat/events{/privacy}",
  "received_events_url": "https://api.github.com/users/octocat/received_events",
  "type": "User",
  "site_admin": false,
  "name": "The Octocat",
  "company": "GitHub",
  "blog": "http://www.github.com/blog",
  "location": "San Francisco",
  "email": null,
  "hireable": null,
  "bio": null,
  "public_repos": 8,
  "public_gists": 8,
  "followers": 2602,
  "following": 9,
  "created_at": "2011-01-25T18:44:36Z",
  "updated_at": "2019-03-22T14:28:22Z"
}
```

### Output struct(s)

```
type root struct {
Login string `json:"login"`
Id int `json:"id"`
NodeId string `json:"node_id"`
AvatarUrl string `json:"avatar_url"`
GravatarId string `json:"gravatar_id"`
Url string `json:"url"`
HtmlUrl string `json:"html_url"`
FollowersUrl string `json:"followers_url"`
FollowingUrl string `json:"following_url"`
GistsUrl string `json:"gists_url"`
StarredUrl string `json:"starred_url"`
SubscriptionsUrl string `json:"subscriptions_url"`
OrganizationsUrl string `json:"organizations_url"`
ReposUrl string `json:"repos_url"`
EventsUrl string `json:"events_url"`
ReceivedEventsUrl string `json:"received_events_url"`
Type string `json:"type"`
SiteAdmin bool `json:"site_admin"`
Name string `json:"name"`
Company string `json:"company"`
Blog string `json:"blog"`
Location string `json:"location"`
Email int `json:"email"`
Hireable int `json:"hireable"`
Bio int `json:"bio"`
PublicRepos int `json:"public_repos"`
PublicGists int `json:"public_gists"`
Followers int `json:"followers"`
Following int `json:"following"`
CreatedAt string `json:"created_at"`
UpdatedAt string `json:"updated_at"`
}
}
```
