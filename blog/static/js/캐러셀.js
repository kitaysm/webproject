$(document).ready(function() {
    function moveToSelected(element) {
        var selected;
        if (element == "next") {
            selected = $(".selected").next();
        } else if (element == "prev") {
            selected = $(".selected").prev();
        } else {
            selected = element;
        }

        var next = selected.next();
        var prev = selected.prev();
        var prevSecond = prev.prev();
        var nextSecond = next.next();

        selected.removeClass().addClass("selected");

        prev.removeClass().addClass("prev");
        next.removeClass().addClass("next");

        nextSecond.removeClass().addClass("nextRightSecond");
        prevSecond.removeClass().addClass("prevLeftSecond");

        nextSecond.nextAll().removeClass().addClass('hideRight');
        prevSecond.prevAll().removeClass().addClass('hideLeft');
    }

    // 키보드 이벤트
    $(document).keydown(function(e) {
        switch(e.which) {
            case 37: // 왼쪽 화살표
                moveToSelected('prev');
                break;
            case 39: // 오른쪽 화살표
                moveToSelected('next');
                break;
            default: return;
        }
        e.preventDefault();
    });

    // 캐러셀 div 클릭 이벤트
    $('#carousel div').click(function() {
        moveToSelected($(this));
    });

    // 버튼 클릭 이벤트
    $('#prev').click(function() {
        moveToSelected('prev');
    });

    $('#next').click(function() {
        moveToSelected('next');
    });
});
