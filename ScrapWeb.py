import requests, pandas
from bs4 import BeautifulSoup

estate = []
basic_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
req = requests.get(basic_url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
content = req.content
soup = BeautifulSoup(content, "html.parser")
div = soup.findAll("div", {"class":"propertyRow"})
pageno = soup.findAll("a", {"class":"Page"})
print(pageno)

for i in range(0, 30, 10):
    req = requests.get(basic_url + str(i) + ".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    div = soup.findAll("div", {"class":"propertyRow"})
    pageno = soup.findAll("a", {"class":"Page"})
    for items in div:
        info = {}
        info["Address"] = items.findAll("span", {"class":"propAddressCollapse"})[0].text
        info["Locality"] = items.findAll("span", {"class":"propAddressCollapse"})[1].text
        info["Price"] = items.find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")

        try:
            info["Beds"] = items.findAll("span", {"class":"infoBed"}).text
        except:
            info["Beds"] = None

        try:
            info["Full Bath"] = items.findAll("span", {"class":"infoValueFullBath"}).text
        except:
            info["Full Bath"] = None

        try:
            info["Half Bath"] = items.findAll("span", {"class":"infoValueHalfBath"}).text
        except:
            info["Half Bath"] = None

        try:
            info["Area"] = items.findAll("span", {"class":"infoSqFt"}).text
        except:
            info["Area"] = None

        for col_group in items.findAll("div", {"class":"columnGroup"}):
            for feature_group,feature_name in zip(col_group.findAll("span", {"class":"featureGroup"}), col_group.findAll("span", {"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    info["Feature"] = feature_name.text

        estate.append(info)

data = pandas.DataFrame(estate)
data.to_csv("RealEstate.csv")