type spatialReference struct {
Wkid int `json:"wkid"`
Latestwkid int `json:"latestWkid"`
}



type root struct {
Spatialreference spatialReference
Candidates []map[string]interface{} `json:"candidates"`
}



