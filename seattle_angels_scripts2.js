var databaseURL   = "https://seattle-angels.firebaseio.com/";
var myFirebaseRef = new Firebase(databaseURL);


function plainTextToHtml(toConvert)
{
	var calcS = toConvert;
	while (calcS.indexOf('\n') != -1)
		calcS = calcS.replace("\n","</div><div>");
	return "<div>" + calcS + "</div>"
}

function initialize()
{
	document.body.innerHTML = loadPage("display_window.html");
	//JET do I need to be listening for other event types? I want to know if _anything_ changes. Do I need to be listening to each event individually?
	myFirebaseRef.child("/").on("value", createRevealPagesHTML); 
}

function createRevealBodyPageHTML(type, cardData, cardAddress)
{
	var calcS;			
	var title = cardData['Title']
	title = title.trim()
	var prefixHTML  = 	"<section id=" + title + ">" +
							"<div class=title>" + title + "</div>"
	var summaryHTML = ""
	var bodyHTML	= ""
	var suffixHTML  = "</section>"
	for (entryType in cardData)
	{
		for (entry in cardData[entryType])
		{
			switch(entryType)
			{
				case "CompanyBriefLogo" :
					prefixHTML += "<img class=textwrap src=\"" + cardData[entryType][entry] + "\">"
					break;
				case "CompanyBriefHeading" :
					if (entry != '<+Untitled+>')
						summaryHTML	+= "<div style=\"font-weight:bold;\">" 	+ entry 										+ "</div>"
					summaryHTML		+= "<div>" 							   	+ plainTextToHtml(cardData[entryType][entry]) 	+ "</div>"
					break;					
				case 'CompanyBriefBody': 
					bodyHTML	+= "<div style=\"font-weight:bold;\">"			+ title 										+ "</div>"
					bodyHTML	+= "<div>" 							  			+ plainTextToHtml(cardData[entryType][entry]) 	+ "</div>"
					break;
				break;
	}	}	}
	return prefixHTML + summaryHTML + bodyHTML + suffixHTML;
	
}
function createRevealPagesHTML(databaseReply)
{
	var cardset;
	var entryNumber;
	var newHTML = "";
	for (cardsetIndex in databaseReply.val()['SAC_9_1']['cardsetOrder'])
	{
		var cardsetName = databaseReply.val()['SAC_9_1']['cardsetOrder'][cardsetIndex]
		if (cardsetName in databaseReply.val()['SAC_9_1'])
		{
			var prefixHTML 			= "";
			var summaryHTML 		= "";
			var summarySuffixHTML 	= "";
			var suffixHTML 			= "";
			var bodyHTML   			= "";
			switch (cardsetName)
			{
				case 'CompanyBriefCards': 
					prefixHTML = 		"<section id=companiesheader>" 	+
											"<section id=companies>"	+
												"<h3>Companies</h3>"	+
												"<div align=left >"		;
					summarySuffixHTML = 	"</div></section>"			;
					suffixHTML = 		"</section>"					;
					break;
				case 'WelcomeMessageCards':
					summaryHTML = databaseReply.val()['SAC_9_1'][cardsetName]
					prefixHTML = ""; suffixHTML = ""; bodyHTML = "";
					break;
				default:
					throw "Error: card type \"" + cardsetName + "\" is not recognized. Please add support for it in this script."
			}
			if (!(typeof databaseReply.val()['SAC_9_1'][cardsetName] == "string") &&
				!(typeof databaseReply.val()['SAC_9_1'][cardsetName] == "number"))
			
			{
				for (entryNumber in databaseReply.val()['SAC_9_1'][cardsetName])
				{
					var entryPath 	=                    "/SAC_9_1/" + cardsetName + "/" + entryNumber
					var entryData 	= databaseReply.val()['SAC_9_1']  [cardsetName]       [entryNumber]
					var title 		= databaseReply.val()['SAC_9_1']  [cardsetName]       [entryNumber]  ['Title']
					title = title.trim()
					switch (cardsetName)
					{
						case 'CompanyBriefCards': 		
							var calcS = "#/" + title
							summaryHTML += "<div class=listelement>	<a href=" + calcS + ">" + title + "</a> </div>"
							bodyHTML += createRevealBodyPageHTML(cardset, entryData, entryPath)
							break;
						default:
							throw "Error: card type \"" + cardsetName + "\" is not expected to be defined as an object type. Please redfine as a string in Firebase"
			}	}	}	
			newHTML += prefixHTML + summaryHTML + summarySuffixHTML + bodyHTML + suffixHTML;
			//console.log(bodyHTML)
	}	}
	
	
	document.getElementById('revealSlidesSection').innerHTML = newHTML;

	Reveal.initialize({
		history: true,

		// More info https://github.com/hakimel/reveal.js#dependencies
		dependencies: [
			{ src: 'plugin/markdown/marked.js' },
			{ src: 'plugin/markdown/markdown.js' },
			{ src: 'plugin/notes/notes.js', async: true },
			{ src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } }
		]
	});


//	<div id="aria-status-div" aria-live="polite" aria-atomic="true" style="position: absolute; height: 1px; width: 1px; overflow: hidden; clip: rect(1px 1px 1px 1px);">  			Welcome 			 				Welcome letter goes here.  		</div>
	
	//<div class="slides" id="revealSlidesSection">
	//var newHTMLHandle = document.createElement('div')
	//newHTMLHandle.id  = "revealSlidesSection"
	//newHTMLHandle.className = "slides"
	//newHTMLHandle.innerHTML = newHTML
	//document.getElementById('revealWrapper').appendChild(newHTMLHandle)
	
	//<div class="reveal" id="revealWrapper">
//	document.getElementById('revealWrapper').className = "reveal"
//	window.getComputedStyle(document.getElementById('revealWrapper'))

	//window.innerWidth = window.innerWidth - 1
	//document.getElementById('revealSlidesSection').width = document.getElementById('revealSlidesSection').width - 
	
	/*
	var element = document.getElementById('revealSlidesSection');
	var n = document.createTextNode(' ');
	var disp = element.style.display;  // don't worry about previous display style
	element.appendChild(n);
	element.style.display = 'none';
	setTimeout(function(){
    	element.style.display = disp;
    	n.parentNode.removeChild(n);
	},20);
	
	
	console.log(window.getComputedStyle(document.getElementById('revealSlidesSection')))
	
	console.log("------------")
	console.log(window.getComputedStyle(document.getElementById('revealSlidesSection')))
	//document.getElementById('revealSlidesSection').style = styleObj
	
	
	//document.getElementById('revealSlidesSection').style = document.getElementById('revealSlidesSection').style
//	forceRedraw(document.getElementById('revealSlidesSection'))
	*/
}

function initialize()
{
	//JET do I need to be listening for other event types? I want to know if _anything_ changes. Do I need to be listening to each event individually?
	myFirebaseRef.child("/").on("value", createRevealPagesHTML); 
}

initialize()