<?php
// Methode 1: Verwendung von dompdf/dompdf
function htmlToPdfDompdf($html, $filename) {
  require_once 'vendor/autoload.php';
  use Dompdf\Dompdf;

  $dompdf = new Dompdf();
  $dompdf->loadHtml($html);
  $dompdf->setPaper('A4', 'portrait');
  $dompdf->render();
  file_put_contents($filename, $dompdf->output());
}

// Beispielaufruf
$html = "<h1>Hello World</h1><p>This is a test PDF.</p>";
$filename = "output.pdf";
htmlToPdfDompdf($html, $filename);
