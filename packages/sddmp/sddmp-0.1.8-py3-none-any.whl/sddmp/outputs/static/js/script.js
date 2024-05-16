$(document).ready(function() {
    $('button[id^="showmore-"]').click(function() {
        var $button = $(this);
        var $list = $button.closest('div.align-items-left').find('ul');

        $list.find('div.hidden:lt(5)').removeClass('hidden');

        var remainingHidden = $list.find('div.hidden').length;
        var unHidden = $list.find('div:not(.hidden)').length;

        console.log("hidden items remaining: " + remainingHidden);
        console.log("unhidden items: " + unHidden);

        if (unHidden >= 5) {
            $button.siblings('button[id^="showless-"]').removeClass('hidden');
        }

        if (remainingHidden === 0) {
            $button.addClass('hidden');
        }
    });

    $('button[id^="showless-"]').click(function() {
        var $button = $(this);
        var $list = $button.closest('div.align-items-left').find('ul');

        var unHidden = $list.find('div:not(.hidden)').length;
        var itemsToHide = unHidden > 10 ? 5 : unHidden - 5;

        $list.find('div:not(.hidden):lt(' + itemsToHide + ')').addClass('hidden');

        var remainingHidden = $list.find('div.hidden').length;
        var unHidden = $list.find('div:not(.hidden)').length;

        console.log("hidden items remaining: " + remainingHidden);
        console.log("unhidden items: " + unHidden);

        if (unHidden <= 5) {
            $button.addClass('hidden');
        }

        if (remainingHidden > 0) {
            $button.siblings('button[id^="showmore-"]').removeClass('hidden');
        }
    });
});