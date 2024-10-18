<?php
require_once('mpdf/autoload.inc.php');

use Mpdf\Mpdf;

function createPDF($html, $filename)
{
  $mpdf = new Mpdf();
  $mpdf->WriteHTML($html);
  $mpdf->Output($filename, 'F');
}

// ... more.
