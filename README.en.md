lingualeo2anki is server, that listen requests from [LinguaLeo English Translator](https://chrome.google.com/webstore/detail/lingualeo-english-transla/nglbhlefjhcjockellmeclkcijildjhi?hl=ru) (you have to modify this plugin) 

How to modify chrome plugin
- make copy, in `lingualeo\js\server.js` change `g+lingualeo.config.ajax.addWordToDict` to `"http://localhost:3000"`
![210601](https://cloud.githubusercontent.com/assets/7573215/8169794/959ce23c-13b4-11e5-8234-6f0c0429e440.png)
or

- you can [download](https://mega.co.nz/#F!8sFHjQZa!Tj0cZnarJo2N24SRFNWVMg) already modified


add plugin to chrome in developer mode
register in lingualeo
run server
add some english word, server will save it to local file, ready for importion to anki

my anki deck look like 

```
Card1
front 
<span style='font-size: 12px;'>{{Question}}</span>
<span style='font-size: 12px; color:#0174DF'>[{{Transcription}}]</span>

styling
.card {
 font-family: arial;
 font-size: 11px;
 text-align: center;
 color: black;
 background-color: white;
}

input[type="button"] {
  font-size: 10px;
}
#syn_tr {
  display: none;
}
back template
{{FrontSide}}
<hr id=answer>
<div style='font-size: 12px;'>{{Answer}}</div>
<span style='color: green'></span>
<div style='color: blue'>{{Context}}</div>
<br>
<img src="{{Image}}">

Card2
front
<div style='font-size: 12px;'>{{Answer}}</div>
styling 
same
back
{{FrontSide}}
<hr id=answer>
<span style='font-size: 12px;'>{{Question}}</span>
<span style='font-size: 12px; color:#0174DF'>[{{Transcription}}]</span>
<div>
<span id="syn" style='color: green'></span>
<div style='color: blue'>{{Context}}</div>
<br>
<img src="{{Image}}">
```
