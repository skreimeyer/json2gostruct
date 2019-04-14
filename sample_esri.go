type spatialReference struct {
wkid int `json:"wkid"`
latestWkid int `json:"latestWkid"`
}



type root struct {
spatialReference spatialReference
candidates []map[string]interface{} `json:"candidates"`
}



