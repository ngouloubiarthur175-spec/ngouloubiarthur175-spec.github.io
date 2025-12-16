// Simple site script from backup
(function(){
  // Fill year
  var y = new Date().getFullYear();
  var el = document.getElementById('year');
  if(el) el.textContent = y;

  // Mobile menu toggle
  var btn = document.getElementById('menu');
  var nav = document.getElementById('nav');
  if(btn && nav){
    btn.addEventListener('click', function(){
      if(nav.style.display === 'block') nav.style.display = '';
      else nav.style.display = 'block';
    });
  }

  // If view PDF button exists, open project PDF in new tab (fallback behaviour)
  var pdfBtn = document.getElementById('viewPdfBtn');
  if(pdfBtn){
    pdfBtn.addEventListener('click', function(e){
      e.preventDefault();
      window.open('PROJET/PROJET2/PROJET.pdf','_blank');
    });
  }

  // Build two QR codes: one for the site and one for Linktree (uses api.qrserver.com)
  try {
    var qrImgSite = document.getElementById('siteQrSite');
    var qrSiteLink = document.getElementById('qrSiteLink');
    var qrImgLink = document.getElementById('siteQrLinktree');
    var qrLink = document.getElementById('qrLink');
    var url = window.location.protocol + '//' + window.location.host + window.location.pathname;

    // Site QR: prefer a data-qr-target on the site link, otherwise use current page URL
    if(qrImgSite && qrSiteLink){
      var siteTarget = qrSiteLink.getAttribute('data-qr-target') || url;
      var qrSrcSite = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + encodeURIComponent(siteTarget);
      qrImgSite.src = qrSrcSite;
      qrSiteLink.href = siteTarget;
    }

    // Linktree QR: prefer data-qr-target on qrLink (existing), otherwise use current page URL
    if(qrImgLink && qrLink){
      var linkTarget = qrLink.getAttribute('data-qr-target') || url;
      var qrSrcLink = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + encodeURIComponent(linkTarget);
      qrImgLink.src = qrSrcLink;
      qrLink.href = linkTarget;
    }
  } catch(e){ /* ignore if DOM not ready */ }
})();