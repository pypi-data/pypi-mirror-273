import os
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


from .template import generate_templates
from .components import  draw_invoice,draw_bill_to,draw_company,draw_line_items,draw_totals, draw_logo, draw_stylish_background
from .io import load_from_yaml, load_config_from_yaml


# Generate PDF Invoice with variables for customization
def generate_pdf(invoice, config,pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Draw stylish background
    #draw_stylish_background(c, width, height)

    draw_logo(c,invoice,config)
    draw_invoice(c, config['left_margin'], height-config['invoice_top'])
    draw_company(c,invoice,config)
    draw_bill_to(c,invoice,config)
    draw_line_items(c,invoice,config)    
    draw_totals(c,invoice,config)
    c.save()


    return invoice

def main():
    parser = argparse.ArgumentParser(prog="invoiceonator",description="Generate an invoice template or invoice PDF from yaml")
    parser.add_argument("--template", action="store_true", help="Generate template YAML file")
    parser.add_argument("--pdf", help="PDF filename to save as, will use invoice number as default filename")
    parser.add_argument("--invoice", help="Invoice yaml ")
    parser.add_argument("--config", help="Config yaml ")

    args = parser.parse_args()
    if args.template:
        generate_templates()
        print("Template YAML file generated successfully.")
    elif  args.invoice and args.config:
        # Generate PDF file from YAML data
        invoice=None
        config=None
        if args.config:        
            if os.path.exists(args.config):
                config = load_config_from_yaml(args.config)
            else:
                print("Missing config.yaml")
                exit(1)

        if args.invoice:        
            if os.path.exists(args.invoice):
                invoice =load_from_yaml(args.invoice)
            else:
                print("Missing invoice.yaml")
                exit(1)
        if args.pdf:
            pdf=args.pdf
        else:
            if invoice['number'] and len(invoice['number'])>1:
                pdf=os.path.join(invoice['number']+".pdf")
            else:
                print("Invoice missing Invoice Number, and no output pdf filename given.")
                exit(1)
        generate_pdf(invoice, config,pdf)
        print("PDF file generated successfully.")
    else:
            parser.error("Either --template or --invoice --config")

        



