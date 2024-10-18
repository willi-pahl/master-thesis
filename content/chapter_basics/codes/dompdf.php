<?php
require 'vendor/autoload.php';

use Dompdf\Dompdf;

function createPDF($html, $filename)
{
  $dompdf = new Dompdf();
  $dompdf->loadHtml($html);
  $dompdf->setPaper('A4', 'portrait');
  $dompdf->render();
  file_put_contents($filename, $dompdf->output());
}

// ... more.
