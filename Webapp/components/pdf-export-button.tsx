"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { DownloadIcon } from 'lucide-react';

interface PDFExportButtonProps {
  reportId: string;
  className?: string;
}

export function PDFExportButton({ reportId, className }: PDFExportButtonProps) {
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    const element = document.getElementById('report-container');
    if (!element) return;
    
    try {
      setExporting(true);
      
      // Dynamically import html2pdf.js only when needed
      const html2pdfModule = await import('html2pdf.js').catch(error => {
        console.error('Error loading html2pdf.js:', error);
        throw new Error('Failed to load PDF export library');
      });
      
      const html2pdf = html2pdfModule.default || html2pdfModule;
      
      const opt = {
        margin: 10,
        filename: `EduVision-Report-${reportId}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };
      
      await html2pdf().set(opt).from(element).save();
    } catch (err) {
      console.error('PDF export failed:', err);
      alert('Could not export to PDF. Please try again later.');
    } finally {
      setExporting(false);
    }
  };

  return (
    <Button 
      onClick={handleExport}
      disabled={exporting}
      className={className || "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 flex items-center gap-2 transition-all duration-200 transform hover:scale-105"}
    >
      <DownloadIcon className="h-4 w-4" />
      {exporting ? 'Exporting...' : 'Export as PDF'}
    </Button>
  );
}