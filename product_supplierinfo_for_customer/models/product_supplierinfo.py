# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        res = super().search_fetch(domain, field_names, offset, limit, order)
        if (
            self.env.context.get("customerinfo")
            and self._name == "product.supplierinfo"
        ):
            limit2 = limit - len(res) if limit else limit
            res2 = self.env["product.customerinfo"].search_fetch(
                domain, field_names, offset, limit=limit2, order=order
            )
            res2 = res2.read(list(self.env["product.supplierinfo"]._fields.keys()))
            for result in res2:
                res += self.env["product.supplierinfo"].new(result)
        return res

    def read(self, fields=None, load="_classic_read"):
        if (
            self.env.context.get("customerinfo")
            and self._name == "product.supplierinfo"
        ):
            has_ids = self.filtered(lambda x: x.id in x._ids and isinstance(x.id, int))
            new_ids = self.filtered(
                lambda x: x.id in x._ids and not isinstance(x.id, int)
            )
            return super(ProductSupplierInfo, has_ids).read(
                fields=fields, load=load
            ) + [
                {f: x[f] for f in x._fields if (f in fields if fields else True)}
                for x in new_ids
            ]
        else:
            return super().read(fields=fields, load=load)
