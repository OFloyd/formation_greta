var iframe = document.getElementById('map');

iframe.addEventListener('load', function() {
  var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
  iframeDocument.addEventListener('click', function() {
    // Your click event code goes here
    console.log('The iframe was clicked!');
  });
});
