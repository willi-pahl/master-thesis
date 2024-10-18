<?php
require_once('tcpdf/tcpdf.php');

class CustomPDF extends TCPDF
{
  public function Header()
  {
    $this->SetFont('helvetica', 'B', 20);
    $this->Cell(0, 15, 'Beispiel-PDF', 0, false, 'C', 0, '', 0, false, 'M', 'M');
  }
}

function createPDF($html, $filename) {
  $pdf = new CustomPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);
  $pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);
  $pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
  $pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
  $pdf->SetFooterMargin(PDF_MARGIN_FOOTER);
  $pdf->setPrintHeader(false);
  $pdf->setPrintFooter(false);
  $pdf->AddPage();
  $pdf->writeHTML($html, true, false, true, false, '');
  $pdf->Output($filename, 'F');
}

// ... more.
