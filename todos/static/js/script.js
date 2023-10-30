document.addEventListener("DOMContentLoaded", function (event) {
    var checkbox = document.querySelector("input[name=switch_completed]");

    checkbox.addEventListener('change', function() {
        if (checkbox.checked){
            const url = new URL(document.location);
            const searchParams = url.searchParams;
            searchParams.delete("disablecompleted");
            window.history.pushState({}, '', url.toString());
            window.location.replace(window.location.href + "?disablecompleted=true");
        } else {
            const url = new URL(document.location);
            const searchParams = url.searchParams;
            searchParams.delete("disablecompleted");
            window.history.pushState({}, '', url.toString());
            window.location.replace(window.location.href + "?disablecompleted=false");
            // location.reload();
        }
    });
});