import os
import locale
from PIL import Image
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter

# Set the locale for formatting (e.g., 'en_US.UTF-8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def format_currency(value):
    return locale.currency(float(value), grouping=True)


# Draw INVOICE text
def draw_invoice(c, x, y):
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(0.2, 0.2, 0.4)  # Light grey
    c.drawString(x, y, "INVOICE")
    c.setFillColorRGB(0.2, 0.2, 0.2)  # Light grey
    c.setFont("Helvetica", 12)

# Draw logo
def draw_logo(c,invoice,config):
    width, height = letter
    if 'logo_path' not in config: 
        return
    
    # Resize and draw logo directly
    logo = Image.open(config['logo_path'])
    aspect_ratio = logo.width / logo.height
    new_width = config['logo_max_width']
    new_height = int(new_width / aspect_ratio)

    # Use ReportLab to draw the image directly, resizing it on the fly
    c.drawImage(config['logo_path'], config['logo_left'], height - config['logo_top'], width=new_width, height=new_height)


# Draw bill section
def draw_bill(c, bill_info, x, y, line_spacing):
    for line in bill_info:
        c.drawString(x, y, line)
        y -= line_spacing  # Adjust spacing between lines

# Draw business information section
def draw_business_info(c, business_info, x, y, line_spacing):
    for line in business_info:
        c.drawString(x, y, line)
        y -= line_spacing  # Adjust spacing between lines

# Function to create a stylish background pattern
def draw_stylish_background(c, width, height):
    # Set a base color for the background
    #c.setFillColorRGB(0.95, 0.95, 0.95)  # Light grey
    #c.rect(0, 0, width, height, fill=1)
    
    # Add a decorative feature, like a colored strip or rectangle, for a modern touch
    c.setFillColorRGB(0.8, 0.8, 0.8)  # Light grey
    c.rect(0, height - 80, width, 90, fill=1,stroke=0)  # Example: A dark grey strip at the top
    
    c.setFillColorRGB(.2, .2, .2)  # Light grey
  
    # These elements provide a modern and stylish look without requiring advanced drawing capabilities


def draw_bill_to(c,invoice,config):
    width, height = letter
    business_info = [
        f"Attention: {invoice['customer']['attention']}",
        f"{invoice['customer']['name']}",
        f"{invoice['customer']['address1']}",
        f"{invoice['customer']['address2']}",
        f"Phone: {invoice['customer']['phone']}",
        f"Email: {invoice['customer']['email']}",
    ]
    draw_bill(c, business_info, config['left_margin'], height - config['bill_top'], config['line_spacing'])

def draw_company(c,invoice,config):
    width, height = letter
    bill_to_info = [
            f"{config['business_info']['name']}",
            f"{config['business_info']['address1']}",
            f"{config['business_info']['address2']}",
            f"Phone: {config['business_info']['phone']}",
            f"Email: {config['business_info']['email']}",
            f"------------------------------------------",
            f"Invoice Number: {invoice['number']}",
            f"Invoice Date: {invoice['date']}",
            f"Period: {invoice['period']}",
        ]
    draw_business_info(c, bill_to_info, width - config['right_margin']- config['business_info_left'], height - config['business_info_top'], config['line_spacing'])

def draw_totals(c,invoice,config):
    width, height = letter
    page_width = width - config['left_margin'] - config['right_margin']
    # Create the totals table
    totals_table_data = [[key.upper(), format_currency(value)] for key, value in invoice['totals'].items()]
    # Change the color of the discount line item to red
    for data_row in totals_table_data:
        if data_row[0] == 'DISCOUNT':
            data_row[1] = '<font color="red">' + data_row[1] + '</font>'


    totals_table_data = [[Paragraph(cell[0]), Paragraph(cell[1])] for cell in totals_table_data]

    totals_table = Table(totals_table_data, colWidths=[100, 70])
    # Apply styles to the totals table
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        # Add a line below each row for a modern look
        ('LINEBELOW', (0, 0), (-1, -2), 1, colors.black),
        # Make the Total row stand out
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.red),  # Making the last row (total) red
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            
    # Calculate the starting position for the totals table
    # 'table_height' should be the height of your main items table, which can be calculated or estimated
    
    # Draw the totals table
    totals_table.wrapOn(c, page_width, config['table_top'])
    totals_table.drawOn(c, width-config['total_table_left'], height-config['total_table_top'])
    # Add footer
    c.drawString(config['left_margin'], config['footer_position'], config['footer'])


def draw_line_items(c,invoice,config):
    width, height = letter
    page_width = width - config['left_margin'] - config['right_margin']
        
    # Define table columns and invoice
    table_data = [['Item', 'Description', 'Quantity', 'Price', 'Total']]
    for row in invoice['items']:
        price_formatted = locale.currency(row['price'], grouping=True)
        total_formatted = locale.currency(row['total'], grouping=True)
        table_data.append([row['item'], row['description'], row['quantity'], price_formatted, total_formatted])

    # Add empty rows if necessary to make total rows 20
    if 'notes' in invoice:
       table_data.append(['', '', '', '',''])

       for row in invoice['notes']:
           table_data.append(['Note', row,'','', ''])

    while len(table_data) < 21:
        table_data.append(['', '', '', '', ''])

    # Calculate column widths
    col_widths = [page_width * w for w in config['col_widths']]

    # Add editable table
    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Adjust the table style for a modern look
    table.setStyle(TableStyle([
        # Apply background color to the header row for distinction (optional)
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        # Set the text color for the header row to white for better readability (optional)
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        # Remove grid lines and borders to achieve a cleaner look
        ('BOX', (0, 0), (-1, -1), 0, colors.white),  # Removes the outer border
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),  # Removes inner grid lines
        # Add a bottom border to each cell in black for a modern look
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
        # Align text to the left for a cleaner look (adjust as necessary)
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        # Set padding in cells for text to breathe (optional, adjust as necessary)
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        # Adjust font size for better readability (optional, adjust as necessary)
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # Right align Price and Total columns
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        # Format Price and Total columns as currency
        ('TEXTCOLOR', (-2, 0), (-1, -1), colors.black),  # Set text color to black
        ('FONTNAME', (-2, 0), (-1, -1), 'Helvetica'),  # Set font name
        ('FONTSIZE', (-2, 0), (-1, -1), 10),  # Set font size
        ('LEFTPADDING', (-2, 0), (-1, -1), 5),  # Add left padding
        ('RIGHTPADDING', (-2, 0), (-1, -1), 5),  # Add right padding
        ('PADDING', (-2, 0), (-1, -1), 0),  # Add overall padding
    ]))


    table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    table.wrapOn(c, page_width, height)
    table.drawOn(c, config['left_margin'], height-config['table_top'] )
    

