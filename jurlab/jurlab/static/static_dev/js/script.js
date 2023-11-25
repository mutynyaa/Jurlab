function openTab(inside) {
    var content = document.getElementsByClassName('content');

    for (var i = 0; i < content.length; i++) {
        content[i].style.display = 'none';
    }

    document.getElementById(inside).style.display = 'block';
	
}

function ActiveTab() {
	let tab_act = document.getElementById('tab_1');
	tab_act.classList.add('active');
};


// ScrollSave / Сохранение позиции страницы

$(window).scroll(function() {
  sessionStorage.scrollTop = $(this).scrollTop();
});

$(document).ready(function() {
  if (sessionStorage.scrollTop != "undefined") {
    $(window).scrollTop(sessionStorage.scrollTop);
  }
});


function ScrollSave(){
	$("form").submit();
}








