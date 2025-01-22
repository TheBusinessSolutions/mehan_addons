# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

class PwaFileConfig(http.Controller):
    def get_pwa_data(self,web_id):
        ''' Manifest file creator for PWA'''
        pwa = request.env['website'].search([('id','=',web_id)])
        big_img = request.website.image_url(pwa,'pwa_big_image')
        small_img = request.website.image_url(pwa,'pwa_small_image')
        return {
                'short_name': pwa.pwa_short_name,
                'name':  pwa.pwa_name,
                'description':pwa.pwa_description,
                'icons': [
                     {
                        'src': small_img,
                        'type': 'image/png',
                        'sizes': '192x192',
                        'purpose': 'any maskable'
                    },
                    {
                        'src': big_img,
                        'type': 'image/png',
                        'sizes': '512x512',
                        'purpose': 'any maskable'
                    }
                ],
                'start_url': '/',
                'background_color': pwa.pwa_bg_color,
                'display': 'standalone',
                'theme_color':pwa.pwa_theme_color,
        }

    @http.route('/manifest/webmanifest', type='http', auth='public', website=True, sitemap=False)
    def pwa_manifest_data(self,**kwargs):
        ''' PWA manifest getter '''
        web_id = kwargs.get('web_id')
        return request.make_response(json.dumps(self.get_pwa_data(web_id)),
            headers=[('Content-Type', 'application/json;charset=utf-8')])

    @http.route('/service-worker-js', type='http', auth='public')
    def service_worker_rendering(self):
        ''' PWA service worker js '''
        return request.render('atharva_theme_base.service_worker',
            headers=[('Content-Type', 'text/javascript;charset=utf-8')])

    @http.route('/offline/page', type='http', auth='public')
    def offline_pwa(self):
        ''' PWA offline page '''
        return request.render('atharva_theme_base.offline_pwa')

    @http.route('/pwa/is_active', type='json', auth='public', website=True)
    def pwa_is_active(self):
        ''' Check PWA is active or not '''
        return request.website.is_pwa_active