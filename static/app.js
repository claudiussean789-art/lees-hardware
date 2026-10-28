const products = window.BUILDMART_PRODUCTS || [];
const cart = new Map();
const $ = (s) => document.querySelector(s);
const money = (n) => 'J$' + Number(n).toLocaleString('en-JM', {maximumFractionDigits:0});
function addToCart(id){const p=products.find(x=>x.id===Number(id));if(!p)return;const line=cart.get(p.id)||{product:p,qty:0};line.qty++;cart.set(p.id,line);renderCart();}
function updateQty(id,delta){const line=cart.get(Number(id));if(!line)return;line.qty+=delta;if(line.qty<=0)cart.delete(Number(id));renderCart();}
function removeLine(id){cart.delete(Number(id));renderCart();}
function renderCart(){const count=[...cart.values()].reduce((s,x)=>s+x.qty,0);$('#cartCount').textContent=count;const items=$('#cartItems');if(!count){items.innerHTML='<p class="empty-cart">Your cart is empty. Add products to build your quote list.</p>';}else{items.innerHTML=[...cart.values()].map(({product:p,qty})=>`<div class="cart-line"><div><b>${p.name}</b><small>${money(p.price)} / ${p.unit}</small><div class="qty-control"><button data-qty="${p.id}" data-delta="-1" aria-label="Decrease quantity">−</button><span>${qty}</span><button data-qty="${p.id}" data-delta="1" aria-label="Increase quantity">+</button></div></div><div><button class="remove-line" data-remove="${p.id}">Remove</button><div class="cart-line-price">${money(p.price*qty)}</div></div></div>`).join('');}
const total=[...cart.values()].reduce((s,x)=>s+x.product.price*x.qty,0);$('#cartTotal').textContent=money(total);}
function openCart() {document.body.classList.add('cart-open');$('#cartDrawer').setAttribute('aria-hidden','false');}
function closeCart(){document.body.classList.remove('cart-open');$('#cartDrawer').setAttribute('aria-hidden','true');}
document.addEventListener('click',e=>{const add=e.target.closest('[data-add]');if(add){addToCart(add.dataset.add);return;}const qty=e.target.closest('[data-qty]');if(qty){updateQty(qty.dataset.qty,Number(qty.dataset.delta));return;}const rem=e.target.closest('[data-remove]');if(rem){removeLine(rem.dataset.remove);return;}const cat=e.target.closest('[data-category-link]');if(cat){$('#categoryFilter').value=cat.dataset.categoryLink;filterProducts();}});
$('#cartOpen').addEventListener('click',openCart);$('#cartClose').addEventListener('click',closeCart);$('#drawerBackdrop').addEventListener('click',closeCart);
function filterProducts(){const term=$('#searchInput').value.toLowerCase().trim();const category=$('#categoryFilter').value;let shown=0;document.querySelectorAll('.product-card').forEach(card=>{const ok=card.dataset.name.includes(term)&&(category==='all'||card.dataset.category===category);card.hidden=!ok;if(ok)shown++;});$('#noResults').hidden=shown!==0;}
$('#searchInput').addEventListener('input',filterProducts);$('#categoryFilter').addEventListener('change',filterProducts);
$('#checkoutBtn').addEventListener('click',()=>{if(!cart.size){closeCart();$('#products').scrollIntoView();return;}const lines=[...cart.values()].map(({product:p,qty})=>`${qty} × ${p.name} (${p.unit})`).join('\n');$('#quoteItems').value=lines;closeCart();$('#quote').scrollIntoView({behavior:'smooth'});$('#quoteItems').focus();});
$('#quoteForm').addEventListener('submit', e=>{
  e.preventDefault();
  const form=e.currentTarget;
  const payload=Object.fromEntries(new FormData(form).entries());
  const number=String(window.BUILDMART_WHATSAPP_NUMBER||'').replace(/\D/g,'');
  if(!number){
    $('#formMessage').textContent='WhatsApp is nearly ready. Add your business WhatsApp number to BUILDMART_WHATSAPP_NUMBER in app.py before using live orders.';
    return;
  }
  const message=[
    'Hello Lee Hardware, I would like to request an order/quote.',
    '',`Name: ${payload.name}`,`Phone: ${payload.phone}`,
    payload.email?`Email: ${payload.email}`:'',
    `Fulfilment: ${payload.fulfilment||'Delivery'}`,
    payload.location?`Location: ${payload.location}`:'',
    '',`Items and quantities:\n${payload.items}`,
    '', 'Please confirm availability, final prices, delivery/pickup details, and payment options.'
  ].filter(Boolean).join('\n');
  const url=`https://wa.me/${number}?text=${encodeURIComponent(message)}`;
  window.open(url,'_blank','noopener,noreferrer');
  $('#formMessage').textContent='WhatsApp opened with your order details. Review the message and press Send in WhatsApp; the order is not confirmed until the store replies.';
});
renderCart();
