Hier ist eine JavaScript Funktion, die ein DIV-Tag mit einer bestimmten Klasse sucht und einen Text hinzufügt:

```javascript
// JavaScript Funktion, die ein DIV mit einer bestimmten Klasse findet und Text hinzufügt
function insertTextInDivWithClass(className) {
    let divElement = document.querySelector('div.' + className);
    if (divElement) {
        divElement.innerText = 'Hallo von der Funktion!';
    } else {
        console.log('Es wurde kein DIV mit der Klasse "' + className + '" gefunden.');
    }
}
```

Du kannst diese Funktion aufrufen und die gewünschte Klasse als Argument übergeben:

```javascript
insertTextInDivWithClass('my-class'); // Ersetze 'my-class' durch deine tatsächliche Klasse
```
