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
```

# What if I need structs from multiple sources and have name collision?

` curl http://someother.api | ./json2gostruct.py -p PREFIX > newfile.go`

with input . . .

```
{
    "kind": "books#volumes",
    "totalItems": 1,
    "items": [
     {
      "kind": "books#volume",
      "id": "yZ1APgAACAAJ",
      "etag": "Wd66FTmnj2I",
      "selfLink": "https://www.googleapis.com/books/v1/volumes/yZ1APgAACAAJ",
      "volumeInfo": {
       "title": "Harry Potter 1 and the Philosopher's Stone",
       "authors": [
        "J. K. Rowling"
       ],
       "publisher": "Bloomsbury Pub Limited",
       "publishedDate": "1997",
       "description": "Harry Potter is an ordinary boy who lives in a cupboard under the stairs at his Aunt Petunia and Uncle Vernon's house, which he thinks is normal for someone like him who's parents have been killed in a 'car crash'. He is bullied by them and his fat, spoilt cousin Dudley, and lives a very unremarkable life with only the odd hiccup (like his hair growing back overnight!) to cause him much to think about. That is until an owl turns up with a letter addressed to Harry and all hell breaks loose! He is literally rescued by a world where nothing is as it seems and magic lessons are the order of the day. Read and find out how Harry discovers his true heritage at Hogwarts School of Wizardry and Witchcraft, the reason behind his parents mysterious death, who is out to kill him, and how he uncovers the most amazing secret of all time, the fabled Philosopher's Stone! All this and muggles too. Now, what are they?",
       "industryIdentifiers": [
        {
         "type": "ISBN_10",
         "identifier": "0747532699"
        },
        {
         "type": "ISBN_13",
         "identifier": "9780747532699"
        }
       ],
       "readingModes": {
        "text": false,
        "image": false
       },
       "pageCount": 223,
       "printType": "BOOK",
       "categories": [
        "Juvenile Fiction"
       ],
       "averageRating": 4.5,
       "ratingsCount": 19,
       "maturityRating": "NOT_MATURE",
       "allowAnonLogging": false,
       "contentVersion": "preview-1.0.0",
       "imageLinks": {
        "smallThumbnail": "http://books.google.com/books/content?id=yZ1APgAACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
        "thumbnail": "http://books.google.com/books/content?id=yZ1APgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
       },
       "language": "en",
       "previewLink": "http://books.google.com/books?id=yZ1APgAACAAJ&dq=isbn:0747532699&hl=&cd=1&source=gbs_api",
       "infoLink": "http://books.google.com/books?id=yZ1APgAACAAJ&dq=isbn:0747532699&hl=&source=gbs_api",
       "canonicalVolumeLink": "https://books.google.com/books/about/Harry_Potter_1_and_the_Philosopher_s_Sto.html?hl=&id=yZ1APgAACAAJ"
      },
      "saleInfo": {
       "country": "US",
       "saleability": "NOT_FOR_SALE",
       "isEbook": false
      },
      "accessInfo": {
       "country": "US",
       "viewability": "NO_PAGES",
       "embeddable": false,
       "publicDomain": false,
       "textToSpeechPermission": "ALLOWED",
       "epub": {
        "isAvailable": false
       },
       "pdf": {
        "isAvailable": false
       },
       "webReaderLink": "http://play.google.com/books/reader?id=yZ1APgAACAAJ&hl=&printsec=frontcover&source=gbs_api",
       "accessViewStatus": "NONE",
       "quoteSharingAllowed": false
      },
      "searchInfo": {
       "textSnippet": "Harry Potter is an ordinary boy who lives in a cupboard under the stairs at his Aunt Petunia and Uncle Vernon&#39;s house, which he thinks is normal for someone like him who&#39;s parents have been killed in a &#39;car crash&#39;."
      }
     }
    ]
   }
```

returns . . .

```
type PREFIXindustryIdentifiers struct {
Type string `json:"type"`
Identifier string `json:"identifier"`
}


type PREFIXreadingModes struct {
Text bool `json:"text"`
Image bool `json:"image"`
}


type PREFIXimageLinks struct {
Smallthumbnail string `json:"smallThumbnail"`
Thumbnail string `json:"thumbnail"`
}


type PREFIXvolumeInfo struct {
Title string `json:"title"`
Authors []string `json:"authors"`
Publisher string `json:"publisher"`
Publisheddate string `json:"publishedDate"`
Description string `json:"description"`
Industryidentifiers []industryIdentifiers `json:"industryIdentifiers"`
Readingmodes PREFIXreadingModes `json:"readingModes"`
Pagecount int `json:"pageCount"`
Printtype string `json:"printType"`
Categories []string `json:"categories"`
Averagerating float64 `json:"averageRating"`
Ratingscount int `json:"ratingsCount"`
Maturityrating string `json:"maturityRating"`
Allowanonlogging bool `json:"allowAnonLogging"`
Contentversion string `json:"contentVersion"`
Imagelinks PREFIXimageLinks `json:"imageLinks"`
Language string `json:"language"`
Previewlink string `json:"previewLink"`
Infolink string `json:"infoLink"`
Canonicalvolumelink string `json:"canonicalVolumeLink"`
}


type PREFIXsaleInfo struct {
Country string `json:"country"`
Saleability string `json:"saleability"`
Isebook bool `json:"isEbook"`
}


type PREFIXepub struct {
Isavailable bool `json:"isAvailable"`
}


type PREFIXpdf struct {
Isavailable bool `json:"isAvailable"`
}


type PREFIXaccessInfo struct {
Country string `json:"country"`
Viewability string `json:"viewability"`
Embeddable bool `json:"embeddable"`
Publicdomain bool `json:"publicDomain"`
Texttospeechpermission string `json:"textToSpeechPermission"`
Epub PREFIXepub `json:"epub"`
Pdf PREFIXpdf `json:"pdf"`
Webreaderlink string `json:"webReaderLink"`
Accessviewstatus string `json:"accessViewStatus"`
Quotesharingallowed bool `json:"quoteSharingAllowed"`
}


type PREFIXsearchInfo struct {
Textsnippet string `json:"textSnippet"`
}


type PREFIXitems struct {
Kind string `json:"kind"`
Id string `json:"id"`
Etag string `json:"etag"`
Selflink string `json:"selfLink"`
Volumeinfo PREFIXvolumeInfo `json:"volumeInfo"`
Saleinfo PREFIXsaleInfo `json:"saleInfo"`
Accessinfo PREFIXaccessInfo `json:"accessInfo"`
Searchinfo PREFIXsearchInfo `json:"searchInfo"`
}


type PREFIXroot struct {
Kind string `json:"kind"`
Totalitems int `json:"totalItems"`
Items []items `json:"items"`
}
```
