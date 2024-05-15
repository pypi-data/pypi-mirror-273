import yaml

def generate_invoice_yaml():
    # Example generic data
    customer_data = {
        "address1": "123 Main St",
        "address2": "Anytown, USA",
        "attention": "John Doe",
        "email": "john@example.com",
        "name": "Example Company",
        "phone": "(555) 555-5555"
    }

    invoice_data = {
        "date": "2024-03-15",
        "number": "INV001",
        "period": "March 2024"
    }

    items_data = [
        {
            "description": "Product A",
            "item": "Product",
            "price": 100,
            "quantity": 2,
            "total": 200
        },
        {
            "description": "Service B",
            "item": "Service",
            "price": 50,
            "quantity": 3,
            "total": 150
        }
    ]

    totals_data = {
        "discount": 0,
        "subtotal": 350,
        "total": 350
    }

    data = {
        "customer": customer_data,
        "date": invoice_data["date"],
        "items": items_data,
        "number": invoice_data["number"],
        "period": invoice_data["period"],
        "totals": totals_data
    }
    with open("invoice_templates.yaml", "w") as file:
        yaml.dump(data, file)



def generate_config_yaml():
    data = {
        "bill_top": 100,
        "business_info": {
            "address1": "1234 Main ST",
            "address2": "Walker, AL, 000001",
            "email": "bob@acme.com",
            "name": "Acme LMTD",
            "phone": "123-456-7890"
        },
        "business_info_left": 180,
        "business_info_top": 40,
        "col_widths": [0.2, 0.5, 0.1, 0.1, 0.1],
        "footer": "Thank you for your patronage.",
        "footer_position": 30,
        "invoice_top": 60,
        "left_margin": 50,
        "line_spacing": 18,
        "logo_max_width": 500,
        "logo_path": "assets/logo.png",
        "logo_top": 20,
        "logo_left": 20,
        "right_margin": 50,
        "table_top": 630,
        "top_margin": 50,
        "total_table_left": 200,
        "total_table_top": 700
    }
    with open("config_templates.yaml", "w") as file:
        yaml.dump(data, file)


def generate_templates():
    generate_invoice_yaml()
    generate_config_yaml()
