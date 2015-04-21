PDFLATEX = pdflatex -shell-escape
DIPLOMA_REPORT_PDF = diploma_report
COURSE_REPORT_PDF = course_report
TITLE_PDF = diploma_title_only
TASK_PDF = diploma_task_only
BIBTEX = bibtex
RM = rm -rf


all: $(DIPLOMA_REPORT_PDF).pdf $(TITLE_PDF).pdf $(TASK_PDF).pdf


$(DIPLOMA_REPORT_PDF).pdf: *.tex
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)
	$(BIBTEX) $(DIPLOMA_REPORT_PDF).aux
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)


$(COURSE_REPORT_PDF).pdf: *.tex
	$(PDFLATEX) $(COURSE_REPORT_PDF)
	$(BIBTEX) $(COURSE_REPORT_PDF).aux
	$(PDFLATEX) $(COURSE_REPORT_PDF)
	$(PDFLATEX) $(COURSE_REPORT_PDF)

$(TITLE_PDF).pdf: *.tex
	$(PDFLATEX) $(TITLE_PDF)


$(TASK_PDF).pdf: *.tex
	$(PDFLATEX) $(TASK_PDF)


cleanall: clean
	$(RM)  *.pdf

.PHONY: clean
clean:
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl _minted* $(DIPLOMA_REPORT_PDF).pdf $(TASK_PDF).pdf $(TITLE_PDF).pdf $(COURSE_REPORT_PDF).pdf
