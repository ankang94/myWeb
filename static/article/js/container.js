$(function () {
    var urlstr = window.location.pathname;
    var param = urlstr.match(/a\/(\d+)/g) + '';
    var aid = param.split('\/')[1];

    // reload pic url
    if (!isNaN(aid)) {
        $('.article_content').find('img').each(function () {
            var name = $(this).attr('src');
            $(this).attr('src', '/media/' + aid + '/' + name);
        });
    }
});
