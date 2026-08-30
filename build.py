#!/usr/bin/env python
"""LUXURY Travel site builder.
Outputs:
  luxury-travel.html : single self-contained file (artifact preview; everything inlined)
  docs/              : deployable static site (index/services/contact + assets/vendor)
"""
import base64, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
DOCS = os.path.join(HERE, 'docs')
TEMPLATE = os.path.join(HERE, 'luxury.template.html')
OUT_SINGLE = os.path.join(HERE, 'luxury-travel.html')

SITE_URL = 'https://0nlymohammed.github.io/luxury-travel/'

def read(p):
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()

def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)

def data_uri(path):
    mime = 'image/png' if path.endswith('.png') else 'image/jpeg'
    with open(path, 'rb') as f:
        b = base64.b64encode(f.read()).decode('ascii')
    return 'data:%s;base64,%s' % (mime, b)

def asset_path(name):
    for ext in ('.jpg', '.png'):
        p = os.path.join(ASSETS, name + ext)
        if os.path.exists(p):
            return p
    print('MISSING asset:', name); sys.exit(1)

def img_tokens(html):
    return set(re.findall(r'\{\{IMG_([a-zA-Z0-9_]+)\}\}', html))

def head_meta(title_ar, desc_ar, desc_en, path=''):
    return (
        '<link rel="icon" type="image/png" href="favicon.png">\n'
        '<meta name="description" content="%s">\n'
        '<meta property="og:title" content="%s">\n'
        '<meta property="og:description" content="%s">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:url" content="%s%s">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    ) % (desc_ar, title_ar, desc_en, SITE_URL, path)

def build_single(main):
    html = main
    html = html.replace('{{THREE_JS}}', read(os.path.join(HERE, 'vendor', 'three.min.js')))
    html = html.replace('{{LAND_DOTS}}', read(os.path.join(HERE, 'land_dots.json')))
    html = html.replace('{{LAND_POLYS}}', read(os.path.join(HERE, 'land_polys.json')))
    for name in img_tokens(html):
        html = html.replace('{{IMG_%s}}' % name, data_uri(asset_path(name)))
    write(OUT_SINGLE, html)
    print('single: %s (%.2f MB)' % (OUT_SINGLE, os.path.getsize(OUT_SINGLE)/1048576.0))

def build_site(main):
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, 'assets'))
    os.makedirs(os.path.join(DOCS, 'vendor'))

    shutil.copy(os.path.join(HERE, 'vendor', 'three.min.js'), os.path.join(DOCS, 'vendor'))
    write(os.path.join(DOCS, 'vendor', 'geo.js'),
          'window.__LAND=%s;' % read(os.path.join(HERE, 'land_dots.json')).strip())

    try:
        from PIL import Image
        Image.open(os.path.join(ASSETS, 'plane3d.png')).resize((64, 48)).save(os.path.join(DOCS, 'favicon.png'))
    except Exception as e:
        print('favicon skipped:', e)

    shared_style = re.search(r'<style>.*?</style>', main, re.S).group(0)
    nav = re.search(r'<header class="nav">.*?</header>', main, re.S).group(0)
    footer = re.search(r'<footer class="footer">.*?</footer>', main, re.S).group(0)
    wa = re.search(r'<a class="wa".*?</a>', main, re.S).group(0)
    nav_sub = re.sub(r'href="#([a-z0-9]+)"', r'href="index.html#\1"', nav)
    nav_sub = nav_sub.replace('href="index.html#services"', 'href="services.html"')
    nav_sub = nav_sub.replace('href="index.html#contact"', 'href="contact.html"')

    used = set()

    def emit(src_html, out_name, meta):
        html = '<!doctype html>\n<html lang="ar" dir="rtl">\n' + src_html
        html = html.replace('{{HEAD_META}}', meta)
        html = html.replace('{{SHARED_STYLE}}', shared_style)
        html = html.replace('{{NAV_SUB}}', nav_sub)
        html = html.replace('{{FOOTER}}', footer)
        html = html.replace('{{WA}}', wa)
        html = html.replace('<script>{{THREE_JS}}</script>', '<script src="vendor/three.min.js"></script>')
        html = re.sub(r'<script>window\.__LAND=\{\{LAND_DOTS\}\};[^<]*</script>',
                      '<script src="vendor/geo.js"></script>', html)
        for name in img_tokens(html):
            p = asset_path(name)
            used.add(p)
            html = html.replace('{{IMG_%s}}' % name, 'assets/' + os.path.basename(p))
        write(os.path.join(DOCS, out_name), html)
        print('site: docs/%s (%d KB)' % (out_name, os.path.getsize(os.path.join(DOCS, out_name))//1024))

    idx = main.replace('<meta charset="utf-8">',
                       '<meta charset="utf-8">\n' + head_meta(
                           'شركة الفخامة للسفر والسياحة',
                           'شركة الفخامة للسفر والسياحة في بغداد: طيران، فنادق، تأشيرات، فورمولا 1، ورحلات مصمّمة. الوكيل الحصري لطيران Air Mediterranean في العراق.',
                           'LUXURY Travel and Tourism, Baghdad. Flights, hotels, visas, Formula 1 and curated journeys. Exclusive GSA for Air Mediterranean in Iraq.'), 1)
    emit(idx, 'index.html', '')

    emit(read(os.path.join(HERE, 'services.template.html')), 'services.html',
         head_meta('خدمات شركة الفخامة', 'العمليات والخدمات الرئيسية لشركة الفخامة للسفر والسياحة: ثماني خدمات متكاملة من بغداد.',
                   'The eight integrated services of LUXURY Travel and Tourism, Baghdad.', 'services.html'))
    emit(read(os.path.join(HERE, 'contact.template.html')), 'contact.html',
         head_meta('تواصل مع شركة الفخامة', 'تواصل مع شركة الفخامة للسفر والسياحة: المنصور، شارع السفارات، بغداد. واتساب على مدار الساعة.',
                   'Contact LUXURY Travel and Tourism: Al-Mansour, Al-Safarat Street, Baghdad. WhatsApp 24/7.', 'contact.html'))

    for p in sorted(used):
        shutil.copy(p, os.path.join(DOCS, 'assets'))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(DOCS) for f in fs)
    print('site total: %.2f MB, assets: %d' % (total/1048576.0, len(used)))

def main():
    main_html = read(TEMPLATE)
    build_single(main_html)
    build_site(main_html)

if __name__ == '__main__':
    main()
