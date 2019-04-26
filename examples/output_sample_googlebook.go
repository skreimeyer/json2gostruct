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


