prompt_string: str = """
Hier sind zwei Beispiele eine JavaScript Funktion die jeweils ein DIV mit Text füllen:
Beispiel 1
```javascript
// JavaScript Funktion, die ein DIV mit einer ID findet und Text hinzufügt
function insertTextInDiv() {
	let divElement = document.getElementById('myDiv');
	divElement.innerText = 'Hallo Welt!';
}
```
Beispiel 2
```javascript
// JavaScript Funktion, die das erste DIV-Element auf der Seite sucht und Text einfügt
function insertTextInFirstDiv() {
	let divElement = document.querySelector('div');
	divElement.innerText = 'Willkommen auf der Webseite!';
}

```
Aufgabe: "Generiere eine JavaScript-Funktion, die ein DIV-Tag mit einer bestimmten Klasse sucht und einen Text einfügt."
"""
