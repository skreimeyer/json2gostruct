type root struct {
login string `json:"login"`
id int `json:"id"`
node_id string `json:"node_id"`
avatar_url string `json:"avatar_url"`
gravatar_id string `json:"gravatar_id"`
url string `json:"url"`
html_url string `json:"html_url"`
followers_url string `json:"followers_url"`
following_url string `json:"following_url"`
gists_url string `json:"gists_url"`
starred_url string `json:"starred_url"`
subscriptions_url string `json:"subscriptions_url"`
organizations_url string `json:"organizations_url"`
repos_url string `json:"repos_url"`
events_url string `json:"events_url"`
received_events_url string `json:"received_events_url"`
type string `json:"type"`
site_admin bool `json:"site_admin"`
name string `json:"name"`
company string `json:"company"`
blog string `json:"blog"`
location string `json:"location"`
email nil `json:"email"`
hireable nil `json:"hireable"`
bio nil `json:"bio"`
public_repos int `json:"public_repos"`
public_gists int `json:"public_gists"`
followers int `json:"followers"`
following int `json:"following"`
created_at string `json:"created_at"`
updated_at string `json:"updated_at"`
}



