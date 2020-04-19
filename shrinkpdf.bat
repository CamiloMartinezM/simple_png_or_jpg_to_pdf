@echo off

set /a dpi = 72

if not "%1" == "" ( 
 if "%1" == "-dpi" (
  set /a dpi = %2
 )
)

shift & shift

REM Shrinks PDFs and puts them in a subdirectory of the first file
REM Usage: shrinkpdf.bat -dpi [dpi] file
 
REM Location of the Ghostscript exectuble
set GSPATH="C:\Program Files\gs\gs9.26\bin\gswin64c.exe"
 
if "%~1"=="" (
 echo Usage: shrinkpdf.bat -dpi [dpi] file
 goto end
)
 
:shrinkPDF
 
@echo "Processing %~nx1"

REM Work the shrinking magic
REM Based on http://www.alfredklomp.com/programming/shrinkpdf/
%GSPATH% ^
   -sDEVICE=pdfwrite ^
   -dCompatibilityLevel=1.3 ^
   -dPDFSETTINGS=/screen ^
   -dNOPAUSE ^
   -dQUIET ^
   -dBATCH ^
   -dEmbedAllFonts=true ^
   -dSubsetFonts=true ^
   -dColorImageDownsampleType=/Bicubic ^
   -dColorImageResolution=%dpi% ^
   -dGrayImageDownsampleType=/Bicubic ^
   -dGrayImageResolution=%dpi% ^
   -dMonoImageDownsampleType=/Bicubic ^
   -dMonoImageResolution=%dpi% ^
   -sOutputFile=output.pdf ^
"%~1"

REM Load the next file
shift
 
REM Are there any more files to shrink?
if "%~1"=="" goto end
 
goto shrinkPDF
 
:end