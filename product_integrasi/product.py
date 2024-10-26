import logging
import requests  # Pindahkan import requests ke sini
from odoo import models, api

# Inisialisasi logger
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        record = super(ProductTemplate, self).create(vals)
        self.sync_to_z(record)
        return record

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for record in self:
            self.sync_to_z(record)
        return res

    def unlink(self):
        for record in self:
            self.sync_to_z(record, delete=True)
        return super(ProductTemplate, self).unlink()

    def sync_to_z(self, record, delete=False):
        # Fungsi untuk mengirim data ke aplikasi Z*
        z_data = {
            'id': record.id,
            'name': record.name,
            'price': record.list_price,
            'description': record.description_sale,
            'delete': delete
        }

        # Kirim data ke aplikasi Z*
        z_api_url = 'https://api.zapp.com/sync/product'  # Ganti dengan URL yang sesuai
        try:
            response = requests.post(z_api_url, json=z_data)
            response.raise_for_status()  # Memicu exception jika status tidak 200

            # Logika jika sukses
            _logger.info(f"Data product '{record.name}' telah disinkronisasi ke Z* dengan ID {record.id}.")
        except requests.exceptions.HTTPError as err:
            # Logika jika gagal
            _logger.error(f"Gagal mengirim data product '{record.name}' ke Z*: {err}. Response: {response.content if response else 'No response'}")
        except Exception as e:
            _logger.error(f"Kesalahan tak terduga saat mengirim data produk '{record.name}' ke Z*: {e}")
