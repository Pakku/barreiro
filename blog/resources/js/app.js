var $ = window.$ = window.jQuery = require('jquery');

function resizeGridItem(item) {
    let grid = document.getElementsByClassName("post-list")[0];
    let rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    let rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
    let rowSpan = Math.ceil((item.querySelector('.content').getBoundingClientRect().height+rowGap)/(rowHeight+rowGap));
    item.style.gridRowEnd = "span " + rowSpan;
}

function resizeAllGridItems() {
    let allItems = document.getElementsByClassName("post");
    for (let x=0;x<allItems.length;x++) {
        resizeGridItem(allItems[x]);
    }
}

function resizeInstance(instance) {
    let item = instance.elements[0];
    resizeGridItem(item);
}

window.onload = resizeAllGridItems;
window.addEventListener("resize", resizeAllGridItems);

allItems = document.getElementsByClassName("post");
for (let x=0;x<allItems.length;x++) {
    imagesLoaded(allItems[x], resizeInstance);
}

$(window).scroll(function(e) {

    // add/remove class to navbar when scrolling to hide/show
    $('.navbar')[$(window).scrollTop() >= 150 ? 'addClass' : 'removeClass']('navbar-hide');

});