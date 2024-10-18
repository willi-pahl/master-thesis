Natürlich! Hier ist ein Beispiel für eine JavaScript-Funktion, die ein `DIV`-Element sucht und Text hinzufügt:

```javascript
function addTextToDiv(selector, text) {
    // Das Element mit dem angegebenen Selektor suchen
    const divElement = document.querySelector(selector);
    
    // Wenn das Element gefunden wurde, fügen Sie den Text hinzu
    if (divElement) {
        divElement.innerText = text;
    } else {
        console.log("Das DIV-Element mit dem angegebenen Selektor wurde nicht gefunden.");
    }
}

// Beispielaufruf der Funktion
addTextToDiv('div', 'Hallo, dies ist ein eingefügter Text.');
```

In diesem Code:
- `selector` ist der CSS-Selektor für das `DIV`-Element.
- `text` ist der Text, den Sie dem `DIV` hinzufügen möchten.
- Die Funktion verwendet `document.querySelector(selector)` um das Element zu finden.
- Wenn das Element gefunden wird, fügt die Funktion `innerText` des Elements den angegebenen Text hinzu.
