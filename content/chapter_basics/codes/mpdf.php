<?php
// Methode 2: Verwendung von mpdf/mpdf
function htmlToPdfMpdf($html, $filename) {
  require_once 'vendor/autoload.php';
  use Mpdf\Mpdf;

  $mpdf = new Mpdf();
  $mpdf->WriteHTML($html);
  file_put_contents($filename, $mpdf->Output('', 'S'));
}

// Beispielaufruf
$html = "<h1>Hello World</h1><p>This is a test PDF.</p>";
$filename = "output.pdf";
htmlToPdfMpdf($html, $filename);
