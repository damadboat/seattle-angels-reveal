from firebase import firebase
from datetime import datetime
import string
import os

parsed = {}
parsed['Templates'] = {
	"CompanyFinalists":     "<h3>Companies</h3>"                                                        +
	                          "<section id=companies>"                                                  +  
	                            "<section id=companiesList>"                                            +
                                "<div style=\"margin-left:20px;margin-right:20px;margin-top:20px;\">" +
                                  "<div style=\"margin-top:10px;vertical-align=top\">"                +
                                    "<div style=\"width:45%;position:relative;float:left;\">"         +
                                      "$$((((${ordering} & 1) == 1)              && "                 +
                                           "(${round}         == \"Finalist\")   && "                 +
                                           "(${cardtype}      == \"Company\")),     "                 +
                                              "<div class=listelement>"                               +
                                              "<a href=#/${entname}>"                                 +
                                                "<img src=${photourl}>"                               +
                                                "${title}"                                            +
                                            "</a></div>)"                                             +
                                    "</div>"                                                          +
                                    "<div style=\"width:45%;position:relative;float:right;\">"        +
                                      "<div align=left>"                                              +
                                        "$$((((${ordering} & 1) == 0)              && "               +
                                             "(${round}         == \"Finalist\")   && "               +
                                             "(${cardtype}      == \"Company\")),     "               +
                                              "<div class=listelement>"                               +
                                                "<a href=#/${entname}>"                               +
                                                  "<img src=${photourl}>"                             +
                                                  "${title}"                                          +
                                              "</a></div>)"                                           +
                                "</div></div></div></div></section>"                                  +
                                "$$(((${round}         == \"Finalist\")   && "                        +
                                      "(${cardtype}      == \"Company\")),     "                      +
                                      "<section id=${title}>"                                         +
                                        "<div class=title>${title}</div>"                             +
                                        "<div><img src=${photourl}></div>"                            +
                                        "<div>${description}</div>"                                   +
                                      "</section>)"                                                   +
                              "</section>"  
	}
#JET testing purposes only
parsed['Cards'] = {
        "id": 13,
        "update": "2016-02-22 15:13:18-08:00",
        "cardtype": "Company",
        "ordering": 1,
        "round": "Finalist",
        "entname": "Aquarium ",
        "first": "Mark",
        "last": "Merrill",
        "contact": "Mark Merrill",
        "title": "Aquarium ",
        "actionurl": "https://gust.com/companies/aquarium",
        "url": "http://www.aquarium.bio",
        "gust": "https://gust.com/companies/aquarium",
        "photourl": "https://media.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAUnAAAAJDM1NzYzOTEyLTU3NjAtNGE5Zi1hODllLTdkYjQyN2YxZDc2MQ.png",
        "description": "\nAquarium allows you to build reproducible, scalable, and transferable experimental workflows integrated with sample tracking, data collection, laboratory activity and supply chain management. \nThe Aquarium Operating System(TM) (Aquarium OS(TM)), a comprehensive cloud-based laboratory operating system that is designed to enable biotechnology researchers to quickly and easily develop, execute, and share highly reproducible experimental workflows;\n\nAquarium Analytics(TM), which leverages data generated within the Aquarium OS(TM) to provide users with highly accurate predictions of workflow outcomes, including time to completion, cost of necessary inputs, and probability of success; and\n\nThe Aquarium Exchange(TM), a community-focused marketplace in which workflows and protocols developed within the Aquarium OS(TM) can be shared among Aquarium users.\n"
    },  {
        "id": 14,
        "update": "2016-02-18 20:58:00-08:00",
        "cardtype": "Company",
        "ordering": 2,
        "round": "Finalist",
        "entname": "Crystal Clear",
        "first": "Ron",
        "last": "Epperson",
        "contact": "Ron Epperson",
        "title": "Crystal Clear",
        "actionurl": "https://gust.com/companies/crystal-clear-technologies-inc",
        "url": "http://crystalclearcleanwater.com",
        "gust": "https://gust.com/companies/crystal-clear-technologies-inc",
        "photourl": "http://crystalclearcleanwater.com/images/cctlogo.jpg",
        "description": "CCT developed patented technology for removing toxic trace metals from wastewater streams in the power plant, metals and food processing industries. Product is an absorbent material based on the technology. The launch market, power plants, is facing new regulations on Se and expensive solutions from incumbent technology providers. Business model is to partner with water treatment companies for market access.\n\n"
    },  {
        "id": 15,
        "update": "2016-02-22 19:16:33-08:00",
        "cardtype": "Company",
        "ordering": 3,
        "round": "Finalist",
        "entname": "Hubb",
        "first": "Allison",
        "last": "Magyar",
        "contact": "Allison Magyar",
        "title": "Hubb",
        "actionurl": "https://gust.com/companies/hubbdotme",
        "url": "http://www.hubb.me",
        "gust": "https://gust.com/companies/hubbdotme",
        "twitter": "hubbdotme",
        "photourl": "https://pbs.twimg.com/profile_images/663835765332291584/NdmwZMN7.jpg",
        "description": "Hubb is a Software as a Service platform that automates the business process for collecting, managing and marketing the abstracts, speakers and sponsors for conferences and meetings.\n" + \
        "It simplifies the process for selecting, managing, and marketing event content so meeting planners save time. From your call for papers to your very last attendee survey, Hubb enables your planning team, selection committee members, track owners, speakers & sponsors to all collaborate on your conference content on our web-based platform. \n" + \
        "We make it easy for speakers and sponsors to upload and manage their own content. Hubb's grading portal makes it simple for your selection committee to score and select the best content anytime, anywhere. Your planning team and track owners will love how fast and easy it is to manage their sessions.\n" + \
        "Want to market your content to attendees? We make that a snap as well.  Hubb, for meeting planners, by meeting planners.\n"
    },  {
        "id": 21,
        "cardtype": "Company",
        "ordering": 4,
        "round": "QuarterFinals",
        "entname": "3axisData",
        "title": "3axisData",
        "actionurl": "http://www.3axisdata.com",
        "url": "http://www.3axisdata.com"
    },  {
        "id": 22,
        "cardtype": "Company",
        "ordering": 5,
        "entname": "Adaptive Plastics Inc.",
        "title": "Adaptive Plastics Inc.",
        "actionurl": "http://www.adaptiveplastics.com/",
        "url": "http://www.adaptiveplastics.com/"
    }
parsed['Presentation'] = [
  "CompanyFinalists"
  ]

#https://github.com/ozgur/python-firebase
firebase = firebase.FirebaseApplication('https://seattle-angels.firebaseio.com', None);
do_write = True

firebasePath = '/'
if do_write :
	try :
		databaseReply = firebase.put(firebasePath, 'SAC_9_2', parsed);
	except :
		print("---------------------------")
		print(parsed)
		print("---------------------------")
		raise ValueError("upload barfed on " + 	"\n\t" + firebasePath)
else :
	print(parsed)