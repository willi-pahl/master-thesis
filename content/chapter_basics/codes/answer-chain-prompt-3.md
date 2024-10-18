Um eine PHP Funktion zu erstellen, die eine HTML-Zeichenkette in einer PDF-Datei speichert, kann die PHP Bibliothek `DomPDF` verwendet werden. Hier ist ein Beispiel, wie Sie dies tun können:

1. Installieren Sie zuerst die DomPDF Bibliothek über Composer:
```bash
composer require dompdf/dompdf
```

2. Erstellen Sie eine PHP Funktion, die die HTML-Zeichenkette enthält und die PDF speichert:

```php
<?php
require_once __DIR__ . '/vendor/autoload.php';

use Dompdf\Dompdf;

function saveHtmlToPdf($html) {
    // Erstellen Sie eine Instanz von Dompdf
    $dompdf = new Dompdf();

    // Setzen Sie die HTML-Inhalte in Dompdf
    $dompdf->loadHtml($html);

    // (Optional) Konfigurieren Sie die PDF Optionen
    $dompdf->setPaper('A4', 'portrait');

    // Rendern Sie das PDF
    $dompdf->render();

    // Speichern Sie das PDF in einer Datei
    $output = $dompdf->output();
    file_put_contents('output.pdf', $output);
}

// Beispiel HTML-Inhalt
$html = '<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Beispielseite</title>
</head>
<body>
    <h1>Hallo Welt!</h1>
    <p>Dies ist ein Beispiel für die Verwendung von DomPDF in PHP.</p>
</body>
</html>';

// Rufen Sie die Funktion auf, um das HTML als PDF zu speichern
saveHtmlToPdf($html);
?>
```

In diesem Beispiel:
1. Wir laden zuerst die DomPDF Bibliothek über Composer.
2. Eine PHP Funktion `saveHtmlToPdf` wird definiert, die eine HTML-Zeichenkette als Parameter enthält.
3. Innerhalb der Funktion erstellen wir eine Instanz von Dompdf und setzen den in der Funktion übergebenen HTML-Inhalt.
4. Wir rendern das PDF und speichern es als `output.pdf`.

Sie können diese Funktion aufrufen und die gewünschte HTML-Zeichenkette an sie übergeben, um eine PDF-Datei zu erstellen und zu speichern.
