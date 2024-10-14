<?php
// Methode 3: Verwendung von TCPDF
function htmlToPdfTcpdf($html, $filename) {
  require_once 'vendor/autoload.php';
  use TCPDF;

  $pdf = new TCPDF(
    PDF_PAGE_ORIENTATION,
    PDF_UNIT,
    PDF_PAGE_FORMAT,
    true,
    'UTF-8',
    false
  );
  $pdf->AddPage();
  $pdf->writeHTML($html, true, false, true, false, '');
  file_put_contents($filename, $pdf->Output('', 'S'));
}

// Beispielaufruf
$html = "<h1>Hello World</h1><p>This is a test PDF.</p>";
$filename = "output.pdf";
htmlToPdfTcpdf($html, $filename);
