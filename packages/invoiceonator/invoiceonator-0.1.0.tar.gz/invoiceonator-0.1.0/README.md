# invoice-o-nator
Create invoices from a templated csv file


## install

```bash
git clone <REPO>
cd REPO
pipenv install
```

## USAGE

```bash
python -m invoiceonator -h
usage: invoiceonator [-h] [--template] [--pdf PDF] [--invoice INVOICE] [--config CONFIG]

Generate an invoice template or invoice PDF from yaml

options:
  -h, --help         show this help message and exit
  --template         Generate template YAML file
  --pdf PDF          PDF filename to save as, will use invoice number as default filename
  --invoice INVOICE  Invoice yaml
  --config CONFIG    Config yaml


invoiceonator --config config_templates.yaml  --invoice invoice_templates.yaml --pdf invoice.pdf
```

## Update

- Added lines for notes
- auto caculate totals on items and total box

## Example PDF

[Example PDF](./INV001.pdf)
