# Lee's Hardware Store

A responsive Flask storefront for Lee's Hardware in Sandy Bay Main, Hanover, Jamaica, configured for Jamaican dollars (JMD), delivery and customer pickup, and WhatsApp order preparation. It includes separate departments for:
- Sand
- Stone & aggregate
- Cement
- Steel & rebar
- Binding wire
- Quarter wire
- Lumber
- Tools
- Paint
- Blocks
- Plumbing equipment
- Doors

The homepage hero uses the Lee's Hardware storefront photo in `public/static/lee-hardware-storefront.jpeg`. The Lee's Hardware logo appears in the header and footer as `public/static/lees-hardware-logo.png`. Product photos are stored in `public/static/products/` and credited on their product cards; source and license details are in [IMAGE-CREDITS.md](./IMAGE-CREDITS.md).

## Run on Windows with Python 3.12

1. Open Command Prompt in the project folder.
2. Install Flask:
   `py -3.12 -m pip install -r requirements.txt`
3. Start the website:
   `py -3.12 app.py`
4. Open `http://127.0.0.1:5000` in your browser.

## Before going live
- Update the contact details and sample product data with your business information.
- Product prices are demo values in Jamaican dollars (J$), not verified live prices.
- WhatsApp order flow opens a pre-filled WhatsApp message for the customer to review and send. Configure your business WhatsApp number before launch: set the `BUILDMART_WHATSAPP_NUMBER` environment variable to the international country code + number with digits only (for Jamaica, usually starts with `1876`), or set the default in `app.py`. Do not include `+`, spaces, or punctuation. The store must reply to confirm the order; opening WhatsApp does not place or confirm an order.
- JMD sample prices are placeholders and must be replaced with your real prices. Configure delivery zones/charges, privacy policy, terms, and HTTPS for production.
- For production, turn off Flask debug mode and deploy behind a production WSGI server.

## Deploy on Vercel
- Import this GitHub repository into a Vercel project. Vercel detects the Flask app in `app.py`; static assets in `public/` are served from the CDN.
- Pushes to the connected `main` branch deploy according to the Vercel project's Git settings.
- Add `BUILDMART_WHATSAPP_NUMBER` in the Vercel project environment variables to enable WhatsApp ordering.
