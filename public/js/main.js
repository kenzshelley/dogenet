$( document ).ready(function() {
  // everything that happens when you toggle the flippage
  $('.flipper').on('click', function() {
    document.querySelector('.flip-container').classList.toggle('enter');
    document.querySelector('.container').classList.toggle('visible');
    document.querySelector('.vertical.flip-container').classList.toggle('flip'); 
    document.querySelector('.bottom.separator').classList.toggle('opened');
    document.querySelector('.top.separator').classList.toggle('opened');
    document.querySelector('.sidebar').classList.toggle('opened');
    document.querySelector('body').classList.toggle('opened');
    $("html, body").animate({ scrollTop: 0 }, "slow");
  });
  // opening the drawer for mobile
  $('#drawer-icon').on('click', function() {
    document.querySelector('.sidebar').classList.toggle('unhidden');
  });
});
