import yaml

def load_config_from_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def save_config_to_yaml(config, yaml_path):
    with open(yaml_path, 'w') as file:
        yaml.dump(config, file)


def load_from_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        invoice = yaml.safe_load(file)
    for item in invoice['items']:
         if 'total' not in item or item['total']==0:
              item['total']=item['price']*item['quantity']

    if invoice['totals']['subtotal'] == 0 and invoice['totals']['total'] == 0:
            # Calculate subtotal by summing up the item totals
            items_data = invoice['items']
            subtotal = sum(item['total'] for item in items_data)
            
            # Subtract discount from total
            total = subtotal-invoice['totals']['discount']

            # Update the totals data in the invoice_data dictionary
            invoice['totals']['subtotal'] = subtotal
            invoice['totals']['total'] = total
        
            # Save the updated totals back to the YAML file
            with open(yaml_path, 'w') as file:
                yaml.dump(invoice, file)
    return invoice
