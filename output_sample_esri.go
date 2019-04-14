type spatialReference struct {
Wkid int `json:"wkid"`
Latestwkid int `json:"latestWkid"`
}


type location struct {
X float64 `json:"x"`
Y float64 `json:"y"`
}


type attributes struct {
}


type candidates struct {
Address string `json:"address"`
Location location `json:"location"`
Score int `json:"score"`
Attributes attributes `json:"attributes"`
}


type root struct {
Spatialreference spatialReference `json:"spatialReference"`
Candidates []candidates `json:"candidates"`
}


