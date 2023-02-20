from odoo import api, models
from werkzeug import urls

class Website(models.Model):
    _inherit = 'website'
    
    @api.model
    def pager(self, url, total, page=1, step=30, scope=5, url_args=None):
        """ Override pager to add ellipsis between current page, and the first or last page """
        res = super(Website, self).pager(url, total, page=page, step=step, scope=scope, url_args=url_args)

        def get_url(page):
            _url = "%s/page/%s" % (url, page) if page > 1 else url
            if url_args:
                _url = "%s?%s" % (_url, urls.url_encode(url_args))
            return _url

        def get_pager(pcurr, ptotal):
            # Expected result
            # current page = 1, total pages = 12
            # 1, 2, 3, ..., 12
            # current page = 2, total pages = 12
            # 1, 2, 3, 4, ..., 12
            # current page = 5, total pages = 12
            # 1, ..., 4, 5, 6, 7, 8, ..., 12
            # current page = 10, total pages = 12
            # 1, ..., 9, 10, 11, 12

            delta = 2
            left = pcurr - delta
            right = pcurr + delta + 1
            pages = []
            pagesWithEllipsis = []

            for page in range(1, ptotal+1):
                if page == 1 or page == ptotal or (page >= left and page < right):
                    pages.append(page)
            
            ellips = False
            for page in pages:
                if ellips:
                    if page - ellips == 2:
                        pagesWithEllipsis.append({'url': get_url(ellips + 1), 'num': ellips + 1})
                    elif page - ellips != 1:
                        pagesWithEllipsis.append({'url': None, 'num': '...'})
                pagesWithEllipsis.append({'url': get_url(page), 'num': page})
                ellips = page

            return pagesWithEllipsis

        res['pages'] = get_pager(res['page']['num'], res['page_count'])

        return res
